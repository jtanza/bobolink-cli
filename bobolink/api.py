import json
import os
import requests

BASE_URL = os.environ.get('BOBO_URL', 'https://api.bobolink.me/v1/')


def get_response(request, parse_json=True):
    try:
        request.raise_for_status()
        return json.loads(request.text) if parse_json else request.text
    except requests.exceptions.HTTPError as e:
        raise Exception(request.text) from e


def signup(email, password):
    req = requests.post(BASE_URL + 'users',
                      json={'email': email, 'password': password})
    return get_response(req, parse_json=False)


def reset_password(email, new_password, token):
    req = requests.put(BASE_URL + 'users/account/password',
                     json={'email': email, 'new': new_password, 'token': token})
    return get_response(req, parse_json=False)


def send_reset_token(email):
    req = requests.put(BASE_URL + 'users/account/password',
                     json={'email': email})
    return get_response(req, parse_json=False)


def get_token(email, password):
    req = requests.get(BASE_URL + 'token', auth=(email, password))
    return get_response(req, parse_json=False)


def add_bookmarks(creds, bookmarks):
    req = requests.post(BASE_URL + 'bookmarks', auth=(creds['email'], creds['token']),
                      json={'urls': bookmarks})
    return get_response(req)


def delete_bookmarks(creds, bookmarks):
    req = requests.delete(BASE_URL + 'bookmarks', auth=(creds['email'], creds['token']),
                        json={'urls': bookmarks})
    return get_response(req)


def get_user_data(creds):
    email = creds['email']
    req = requests.post(BASE_URL + 'users/search', auth=(email, creds['token']),
                      json={'email': email})
    return get_response(req)


def get_user_bookmarks(creds):
    user = get_user_data(creds)
    req = requests.get(f'{BASE_URL}users/{user["id"]}/bookmarks',
                     auth=(creds['email'], creds['token']))
    return get_response(req)


def search_bookmarks(creds, query, field=None):
    if field is None:
        field = 'content'
    req = requests.post(BASE_URL + 'bookmarks/search', auth=(creds['email'], creds['token']),
                      json={'query': query, 'field': field})
    return get_response(req)
