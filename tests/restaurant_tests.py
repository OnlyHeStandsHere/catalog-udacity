import requests
import json

# first we'll set up all the urls we need to test
url_base = "http://localhost:5000"

new_user_url = url_base + "/users"

# these urls will all be tested for get requests
get_urls = [
    '/restaurants/',
    '/restaurant/new',
    '/restaurant/1/edit/',
    '/restaurant/1/delete',
    '/restaurant/1/menu',
    '/restaurant/1/menu/new',
    '/restaurant/1/menu/1/edit',
    '/restaurant/1/menu/1/delete',
]

# these urls will all be tested for POST requests
post_urls=[

]

# a user to test user creation via json
params = {
    'username': "wolf_man_jon",
    'password': 'password123',
    'email': "wolf_man@example.com"
}


# Test 1. Check that all URLS respond to GET Request that do not require a login
print("Test 1: Checking GET Requests for URLs that do not require a log in")
for url in get_urls:
    r = requests.get(url=url_base + url)
    if r.ok:
        print("PASS: GET request to {} Response {} ".format(url, r.status_code))
    else:
        print("FAIL: GET request to {} Response {} ".format(url, r.status_code))


# Test 2. Create a user via json request. This is to test the json api
print("Test 2: Creating a user via json request to /users")