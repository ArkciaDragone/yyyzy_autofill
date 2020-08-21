import requests
import json
from bs4 import BeautifulSoup
from random import random
from datetime import date
from pprint import pprint

SETTINGS = None
URLs = None


def load_settings(settings_file='settings.json', private_file='private.json'):
    global SETTINGS, URLs
    with open(settings_file, encoding='utf-8') as f:
        SETTINGS = json.load(f)
        URLs = SETTINGS['urls']
    try:
        with open(private_file, encoding='utf-8') as f:
            private = json.load(f)
    except FileNotFoundError:
        private = {'userName': input('学号: '),
                'password': input('密码: ')}
        with open(private_file, 'w', encoding='utf-8') as f:
            json.dump(private, f, indent=4)
    SETTINGS['login_data']['userName'] = private['userName']
    SETTINGS['login_data']['password'] = private['password']


def get_session():
    session = requests.Session()
    session.headers = SETTINGS['headers']
    return session


def __save_as_html(resp):
    with open(f"debug.html", 'wb') as f:
        f.write(resp.content)


def login(s):
    s.head(URLs['login_portal'])
    s.head(URLs['login_oauth'])
    json = s.post(URLs['login_post'], SETTINGS['login_data']).json()
    assert json['success'], 'login failed, please check private.json'
    s.head(f'{URLs["login_do"]}?_rand={random()}&token={json["token"]}')


def update_check(session):
    """Check whether data format has changed"""
    resp = session.get(URLs['app_entry'])
    soup = BeautifulSoup(resp.content, 'lxml')
    for script in soup.find_all('script'):
        if 'Yqfk.js' in script.get('src', ''):
            s = script
            break
    else:
        assert False, 'Yqfk.js not found'
    yqfk = session.get(URLs['ssop'] + s['src'])
    if yqfk.headers['Last-Modified'] != SETTINGS['yqfk_version']:
        print('Warning: Yqfk.js has been modified')
    js = str(yqfk.content, encoding='utf-8')
    js = js[js.index('saveMrtb:'):]
    js = js[js.index('reqData'):]
    req = js[js.index('{')+3:js.index('}')].replace(' ', '').replace('\t', '')
    keys = set(filter(lambda x: '//' not in x,
                      (l.split(':')[0] for l in req.splitlines())))
    assert keys == set(SETTINGS['upload_data'].keys()),\
        'ATTENTION REQUIRED: reqData format changed'


def get_today_upload_data(session):
    data = SETTINGS['upload_data']
    json = session.get(URLs['app_info']).json()
    for k in data.keys():
        if json['zrtbxx'].get(k):
            data[k] = json['zrtbxx'][k]
    data['tbrq'] = date.today().strftime('%Y%m%d')  # important
    return data


def upload(session):
    data = get_today_upload_data(session)
    pprint(data)
    if 'required' in data.values():
        print('Some of the "required" items are not filled. ' +
              'Please fill and save the form manually for once and/or modify settings.')
    else:
        print('The following data will be uploaded:')
        ins = input('Confirm? [y]|n:').strip().lower()
        if ins == '' or ins[0] == 'y':
            json = session.post(URLs['app_post']).json()
            assert json['success'], 'upload failure: ' + \
                json.get('msg', 'no msg')
        else:
            print('Aborted.')


if __name__ == "__main__":
    load_settings()
    session = get_session()
    print('Loading...')
    login(session)
    update_check(session)
    upload(session)
