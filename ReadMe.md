# Udacity FSND - Catalog Project

## This project uses python 3 and a provisioned vagrant machine

To get started use the provided vagrant file and provision a machine by typing

    vagrant up
in the project root /catalog directory. This will provision and install
all necessary Python 3 packages to run this project. 

log in to the vagrant machine with the default credentials \

User : vagrant \
Password : vagrant

once logged in to the vagrant machine cd to the vagrant shared directory

/vagrant

you should now be able to run

    python3 run.py

this should get the flask server up and running. The project should be accessable from \
your local machine on

    http://localhost:5000/restaurants
    
## Google OAuth2

This project uses OAuth2 google login. For this to work, you must provide your own
secrets.json file as generated from the google developer console. 

create a directory called /google, and call your file google_login.json

    /google/google_login.json
    
Alternatively, the google secrets is initiallized in 

    /controllers/__init__.py
    
    # location of the google log in secrets file for OAuth2
    CLIENT_SECRET_FILE = "./google/google_login.json"
  
change the CLIENT_SECRET_FILE to where ever else you feel this file should go.
if this is not configured, then log in with google will not work

## Database

An sqlite database in included in the repo so no further action needs to be taken.

## Test User

There is a test user in the database that can be used for making api requests

username : wolf_man_jon \
password: password123

## API URLs

To create a new user submit a post request to

    http://localhost:5000/users
    
This route expects paramaters 

    username, password

A request for an API token can then be made to

    http://localhost:5000/restaurants/token


    