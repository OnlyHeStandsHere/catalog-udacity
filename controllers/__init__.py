# controllers __init__ file
from flask_httpauth import HTTPBasicAuth

# location of the google log in secrets file for OAuth2
CLIENT_SECRET_FILE = "./google/google_login.json"

# this allows the auth object to be imported to
# controller files as it is needed
auth = HTTPBasicAuth()




