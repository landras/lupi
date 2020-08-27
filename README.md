# LUPI
Least Unique Positive Integer

Overview
--------
This project demonstrates a REST API for the game Least Unique Positive Integer.

This is a multiplayer game. Each player picks a positive integer. The lowest unique integer wins. 

It was my test assignment for an applied job. The focus was on planning and implementing of the API, so it has a very basic UI.

The application was written in Python with Flask and Connexion and the UI using Vue.js and jQuery.

How to use it?
--------------
1. Create a virtualenv:
    
        $ virtualenv --system-site-packages --python=/usr/bin/python3 ./env
        
2. Activate the virtualenv:

        $ source env/bin/activate
        
3. Install the requirements:

        $ pip install -r requirements.txt

4. Create the SQLite database:

        $ python3 lupi_app/build_database.py 
        
5. Run the server:

        $ python3 lupi_app/main.py

6. Open the UI in a browser (http://localhost:5000/)

API documentation
-----------------
See on http://localhost:5000/api/ui/

Warning
-------
Do not use the Flask development server in production.

