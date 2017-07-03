import random
import string


# return a 32 char string we will use as the "state"
def get_state():
    rand = ''
    for i in range(32):
        rand += random.choice(string.ascii_uppercase + string.digits)
    return rand


def get_random_char():
    return random.choice(string.ascii_letters + string.digits)