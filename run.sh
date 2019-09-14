#!/bin/bash 
sudo apt-get -f install 
sudo apt-get install python3.7
sudo apt-get install python3-pip 
sudo pip3 install virtualenv
virtualenv -p python3.7 venv
source venv/bin/activate
pip3 install -r requirements.txt
python3.7 app.py

