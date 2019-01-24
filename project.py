from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, airline, equipment
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import jsonify
import json
from flask import make_response
import requests
app = Flask(__name__)

#connect to client_secret.json file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Web client 1"

engine = create_engine('sqlite:///airline.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

    # DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
 	print 'Access Token is None'
    	response = make_response(json.dumps('Current user not connected.'), 401)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
	del login_session['access_token']
    	del login_session['gplus_id']
    	del login_session['username']
    	del login_session['email']
    	del login_session['picture']
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:

    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response


#JSON objects
@app.route('/airline/JSON')
def airlineJSON():
    airlines = session.query(airline).all()
    return jsonify(airlines=[r.serialize for r in airlines])

@app.route('/airline/<int:airline_id>/equipment/JSON')
def equipmentJSON(airline_id):
    airlines = session.query(airline).filter_by(id=airline_id).one()
    equipments = session.query(equipment).filter_by(airline_id=airlines.id).all()
    return jsonify(equipments_list=[i.serilaize for i in items])



# first page showing all the airlines in ascending order


@app.route('/')
@app.route('/airline/')
def showairlines():
    showairlines = session.query(airline).all()
    return render_template('airlines.html', airlines=showairlines)


#create new airline
@app.route('/airline/new/', methods=['GET','POST'])
def newairline():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newairline = airline(name=request.form['name'])
        session.add(newairline)

        session.commit()
        return redirect(url_for('showairlines'))
    else:
        return render_template('newairline.html')

#edit an airline
@app.route('/airline/<int:airline_id>/edit/', methods=['GET','POST'])
def editairline(airline_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedairline = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedairline.name = request.form['name']

            return redirect(url_for('showairlines'))
    else:
        return render_template('editairline.html', airlines=editedairline)


# delete airline
@app.route('/airline/<int:airline_id>/delete/', methods=['GET','POST'])
def deleteairline(airline_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteairline = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        session.delete(deleteairline)

        session.commit()
        return redirect(url_for('showairlines'))
    else:
        return render_template('deleteairline.html', airlines=deleteairline)


# page showing equipments for associated airline

@app.route('/airline/<int:airline_id>/equipment')
def showequipment(airline_id):
    airlines = session.query(airline).filter_by(id=airline_id).one()
    equipments = session.query(equipment).filter_by(airline_id=airlines.id).all()
    return render_template('showequipment.html',equipments=equipments,airlines=airlines)

#create a new equipment1
@app.route('/airline/<int:airline_id>/equipment/new', methods=['GET','POST'])
def newequipment(airline_id):
    if 'username' not in login_session:
        return redirect('/login')
    airlines = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        newequipment= equipment(name=request.form['name'], airline_id=airlines.id)
        session.add(newequipment)
        session.commit()

        return redirect(url_for('showequipment', airline_id=airline_id))
    else:
        return render_template('newequipment.html', airline_id=airlines.id)

#edit an equipment
@app.route('/airline/<int:airline_id>/equipment/<int:equipment_id>/edit/', methods=['GET','POST'])
def editequipment(airline_id, equipment_id):
    if 'username' not in login_session:
        return redirect('/login')
    airlines = session.query(airline).filter_by(id=airline_id).one()
    editequipment = session.query(equipment).filter_by(airline_id=airlines.id).filter_by(id=equipment_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editequipment.name = request.form['name']
        session.add(editequipment)
        session.commit()

        return redirect(url_for('showequipment', airline_id=airlines.id))
    else:
        return render_template('editequipment.html', airlines =airlines, editedequipment=editequipment)

#delete an equipment
@app.route('/airline/<int:airline_id>/equipment/<int:equipment_id>/delete/', methods=['GET','POST'])
def deleteequipment(airline_id,equipment_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteequipment = session.query(equipment).filter_by(id=equipment_id).one()
    if request.method == 'POST':
        session.delete(deleteequipment)
        session.commit()

        return redirect(url_for('showequipment', airline_id=airline_id))
    else:
        return render_template('deleteequipment.html',equipment_id=equipment_id)









if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug= True
    app.run(host='0.0.0.0', port=8000)
