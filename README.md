# Intro to Airline Project
Full stack web development practice project. The focus is to create a RESTful website for airlines and their equipment using Flask, SQLalchemy, oauth apis, html, css, ajax and json. 

## Setup
The following are the steps required to set up the project

### 1. Vagrant
The first requirement is vagrant virtual machine, it can be downloaded at this link https://www.vagrantup.com/downloads.html

### 2. VM
Next we need Virtual machine box to run vagrant the link can be found here: https://www.virtualbox.org/wiki/Downloads

### 3. Vagrant setup file
The vagrant set up file is in folder as "Vagrantfile", download the repositry and place it in a folder where you want to install the vagrant VM and run the project.

### 4. Install Vagrant
In linux or gitbash go to the  folder you placed the "Vagrantfile" from step 3. And type the code below
```
vagrant up
```

### 5. Connecting to Vagrant
Once the vagrant is done installing, we now can connect to via SSH. Type the code below into linux where vagrant is installed:
```
vagrant ssh
```
### 6. Configuring through vagrant
Once you connect to your Vagrant VM via SSH. Now you have to move to the folder where you downloaded and extract the repositry. Type the code below to change directory to where you installed the file "Vagrantfile". 
```
cd /vagrant
```
### 7. Running the project
To run the project, you just need to type the code below and it will deploy as a local website.
```
python project.py
```
### 8. Accessing the website
To access the website go to 
```
localhost:8000
```
