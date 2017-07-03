from models import db
from controllers.helpers import get_state
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context


# generate an api secret key.
# reuse the get_state() method as it will generate a random 32 char string
api_secret_key = get_state()


class User(db.Model):
    """ SQL Alchemy User model"""
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.Integer, nullable=True, index=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), nullable=False, index=True)
    picture = db.Column(db.String(250), nullable=True)
    username = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(80), nullable=True)

    def __init__(self, email, name=None, picture=None, username=None):
        """ user constructor. All parameters are mandatory """
        self.name = name
        self.email = email
        self.picture = picture
        self.username = username

    def __repr__(self):
        """ assigns the user object a name of a restaurant """
        return '<User:{}>'.format(self.name)

    def hash_password(self, password):
        """ hashes a password before db storage """
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """ validates a users password """
        if pwd_context.verify(password, self.password_hash):
            return True

    def generate_auth_token(self, expiration=600):
        """ generates an encrypted token along with 'this' user ID. """
        s = Serializer(api_secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def create_user(login_session):
        """ Creates a new user from available user info stored in a flask.session object """
        user_id = login_session.get('id')
        name = login_session.get('name')
        email = login_session.get('email')
        picture = login_session.get('picture')
        user = User(user_id, name, email, picture)
        db.session.add(user)
        db.commit()

    @staticmethod
    def check_user_existence(login_session):
        """ Checks to see if a user exists in the data base. if so return the user """
        email = login_session.get('email')
        user = db.session.query(db.exists().where(User.email == email)).scalar()
        if user:
            return user

    @staticmethod
    def verify_token(token):
        """ verifies the authenticity of the api access token """
        t = Serializer(api_secret_key)
        try:
            token_data = t.loads(token)
        except BadSignature:        # token is not valid
            print('bad signature')
            return None
        except SignatureExpired:    # token is valid, but has expired
            print("signature expired")
            return None
        return token_data['id']