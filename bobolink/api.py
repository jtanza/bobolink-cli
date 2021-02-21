import json
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


def delete_bookmarks(creds, bookmarks):
    r = requests.delete(BASE_URL + 'bookmarks', auth=(creds['email'], creds['token']),
                      json={'urls': bookmarks})
    return raise_bad_request(r)


def get_user_data(creds):
    email = creds['email']
    r = requests.post(BASE_URL + 'users/search', auth=(email, creds['token']),
                      json={'email': email})
    return raise_bad_request(r)


def get_user_bookmarks(creds):
    user = json.loads(get_user_data(creds))
    r = requests.get(f'{BASE_URL}users/{user["id"]}/bookmarks',
                     auth=(creds['email'], creds['token']))
    return json.loads(raise_bad_request(r))


def search_bookmarks(creds, query, field='content'):
    r = requests.post(BASE_URL + 'bookmarks/search', auth=(creds['email'], creds['token']),
                      json={'query': query, 'field': field})
    return json.loads(raise_bad_request(r))
