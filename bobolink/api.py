import requests

BASE_URL = 'http://localhost:3000/'

def raise_bad_request(request):
    try:
        request.raise_for_status()  
        return request.text      
    except requests.exceptions.HTTPError as e:
        raise Exception(request.text) from e    


def signup(email, password):
    r = requests.post(BASE_URL + 'users', json={'email':email, 'password':password})    
    return raise_bad_request(r)


def get_token(email, password):
    r = requests.get(BASE_URL + 'token', auth=(email, password))
    return raise_bad_request(r)


def add_bookmarks(creds, bookmarks):
    r = requests.post(BASE_URL + 'bookmarks', auth=(creds['email'], creds['token']), 
                      json={'urls': bookmarks})
    return raise_bad_request(r)
