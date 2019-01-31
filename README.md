# Intro to Airline Project
Full stack web development practice project. The focus is to create a RESTful website for airlines and their equipment using Flask, SQLalchemy, oauth apis, html, css, ajax and json. 

## Setup
The following are the steps required to set up the project

### 1. Vagrant
The first requirement is vagrant virtual machine, it can be downloaded at this link https://www.vagrantup.com/downloads.html

### 2. VM
Next we need Virtual machine box to run vagrant the link can be found here: https://www.virtualbox.org/wiki/Downloads

### 3. Vagrant setup file
The vagrant set up file is in folder as "Vagrantfile", download the file and place it in a folder where you want to install the vagrant VM.

### 4. Install Vagrant
In linux or gitbash go to the  folder you placed the "Vagrantfile" from step 3. And type the code below
'''
vagrant up
'''

### 5. Connecting to Vagrant
Once the vagrant is done installing, we now can connect to via SSH. Type the code below into linux where vagrant is installed:
'''
vagrant ssh
'''

