from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, airline, equipment

app = Flask(__name__)

engine = create_engine('sqlite:///airline.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
#JSON objects
@app.route('/airline/JSON')
def airlineJSON():
    airlines = session.query(airline).all()
    return jsonify(airlines=[r.serialize for r in airlines])

@app.route('/airline/<int:airline_id>/equipment/JSON')
def equipmentJSON(airline_id):
    equipments = session.query(equipment).filter_by(airline_id=airline_id).all()
    return jsonify(equipments_list=[i.serilaize for i in items])

@app.route('/airline/<int:airline_id>/equipment/<int:menu_id>/JSON')
def equipmentJSON(airline_id):
    equipments = session.query(equipment).filter_by(airline_id=airline_id).one()
    return jsonify(equipments_list=[i.serilaize for i in equipments])
"""

# first page showing all the airlines in ascending order


@app.route('/')
@app.route('/airline/')
def showairlines():
    showairlines = session.query(airline).order_by(asc(airline.name)).all()
    return render_template('airlines.html', airlines=showairlines)


#create new airline
@app.route('/airline/new/', methods=['GET','POST'])
def newairline():
    if request.method == 'POST':
        newairline = airline(name=request.form['name'])
        session.add(airline)
        flash('New Airline %s is successfully created' % newairline.name)
        session.commit()
        return redirect(url_for('showairlines'))
    else:
        return render_template('newairline.html')

#edit an airline1
@app.route('/airline/<int:airline_id>/edit/', methods=['GET','POST'])
def editairline(airline_id):
    editedairline = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedairline.name = request.form['name']
            flash('airline %s is successfully edited' % editedairline.name)
            return redirect(url_for('showairlines'))
    else:
        return render_template('editairline.html', airline=editedairline)


# delete airline
@app.route('/airline/<int:airline_id>/delete/', methods=['GET','POST'])
def deleteairline(airline_id):
    deleteairline = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        session.delete(deleteairline)
        flash('%s is successfully deleted' % deleteairline.name)
        session.commit()
        return redirect(url_for('showairlines'))
    else:
        return render_template('deleteairline.html', airline=deleteairline)


# page showing equipments for associated airline

@app.route('/airline/<int:airline_id>/equipment')
def showequipment(airline_id):
    airlines = session.query(airline).filter_by(id=airline_id).one()
    equipments = session.query(equipment).filter_by(airline_id=airline_id).all()
    return render_template('showequipment.html',equipments=equipments,airlines=airlines)

#create a new equipment1
@app.route('/airline/<int:airline_id>/equipment/new', methods=['GET','POST'])
def newequipment(airline_id):
    airline = session.query(airline).filter_by(id=airline_id).one()
    if request.method == 'POST':
        newequipment= equipment(name=request.form['name'], airline_id=airline_id)
        session.add(newequipment)
        session.commit()
        flash('new equipment %s is successfully created' % newequipment.name)
        return redirect(url_for('showequipment'), airline_id=airline_id)
    else:
        return render_template('newequipment.html', airline_id=airline_id)

#edit an equipment
@app.route('/airline/<int:airline_id>/equipment/<int:equipment_id>/edit/', methods=['GET','POST'])
def editequipment(airline_id):
    airline = session.query(airline).filter_by(id=equipment_id).one()
    editequipment = session.query(equipment).filter_by(airline_id=airline_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editequipment.name = request.form['name']
        session.add(editequipment)
        session.commit()
        flash('equipment %s is successfully edited' % editequipment.name)
        return redirect(url_for('showequipment', airline_id=airline_id))
    else:
        return render_template('editequipment.html', airline_id=airline_id, equipment_id=equipment_id)

#delete an equipment
@app.route('/airline/<int:airline_id>/equipment/<int:equipment_id>/delete/', methods=['GET','POST'])
def deleteairline(airline_id,equipment_id):
    airline = session.query(airline).filter_by(id=equipment_id).one()
    deleteequipment = session.query(equipment).filter_by(airline_id=airline_id).one()
    if request.method == 'POST':
        session.delete(deleteequipment)
        session.commit()
        flash('airline %s is successfully deleted' % deleteequipment.name)
        return redirect(url_for('showequipment', airline_id=airline_id))
    else:
        return render_template('deleteequipment',equipment_id=equipment_id)









if __name__ == '__main__':

    app.debug= True
    app.run(host='0.0.0.0', port=8000)
