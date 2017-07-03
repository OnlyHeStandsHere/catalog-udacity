from flask import Blueprint, render_template, url_for, redirect, request, flash, make_response, jsonify, abort
from flask import session as login_session
from .helpers import get_state
from controllers import CLIENT_SECRET_FILE
import json
from oauth2client import client
import requests
from models import db
from models.users import User

login = Blueprint("login", __name__)


# A route to accept users from a JSON post
@login.route('/users', methods=['POST'])
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # first check to see if the user already exists
    # if it does return an error, if not, create the new user
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"error": "That User Already Exists"}), 501
    else:
        if username and email and password:
            user = User(username=username,
                        email=email)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'username': user.username}), 201
        else:
            abort(400)


@login.route("/login")
def show_login():
    state = get_state()
    login_session["state"] = state
    return render_template("sessions/login.html", version=get_state(), oauth_state=state)


@login.route("/google_login", methods=['POST'])
def google_login():
    client_state = request.args.get('state')
    if client_state == login_session.get('state'):
        code = request.data

        try:
            credentials = client.credentials_from_clientsecrets_and_code(CLIENT_SECRET_FILE,
                                                                         ["https://www.googleapis.com/auth/plus.login"],
                                                                         code)
        except client.FlowExchangeError:
            response = make_response(json.dumps("Unable to authenticate with Google."), 500)
            response.headers["Content-Type"] = "application/json"
            return response

        login_session['id'] = credentials.id_token["sub"]
        login_session['token'] = credentials.access_token
        login_session['email'] = credentials.id_token['email']
        print(login_session['token'])

        # now make a request for the username
        url = " https://www.googleapis.com/oauth2/v1/userinfo"
        params = {"access_token": credentials.access_token, 'alt': 'json'}
        r = requests.get(url, params=params)

        login_session['user_name'] = r.json().get('name')
        login_session['picture'] = r.json().get('picture')

        print(login_session['user_name'])

        # if the user doesn't already exist in the db, lets create them
        user = User.check_user_existence(login_session)
        if not user:
            print('Create the user')
            user_id = login_session.get('id')
            name = login_session.get('user_name')
            email = login_session.get('email')
            picture = login_session.get('picture')
            user = User(user_id=user_id, name=name, email=email, picture=picture)
            db.session.add(user)
            db.session.commit()

        flash("Your are now logged in as {}".format(login_session['email']))
        return url_for('restaurant.index')
    else:
        response = make_response(json.dumps("There was a problem processing your request"), 500)
        response.headers["Content-Type"] = "application/json"
        return response


@login.route("/logout")
def google_logout():
    access_token = login_session.get('token')
    if access_token:
        url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(access_token)
        r = requests.get(url)
        if r.ok:
            del login_session['token']
            del login_session['id']
            del login_session['email']
            print("You have been logged out")

            flash("You Have Been Logged Out!")
            return redirect(url_for("restaurant.index"))
        else:
            response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        response = make_response(json.dumps('The user is not logged in, unable to log out.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
