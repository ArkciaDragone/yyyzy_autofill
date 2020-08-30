import requests
import json
import argparse
from getpass import getpass
from bs4 import BeautifulSoup
from random import random
from datetime import date
from pprint import pprint

SETTINGS = None
URLs = None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Upload yyyzy data for today.')
    parser.add_argument('-y', '--confirm', action='store_true',
                        help='skip user confirmation; useful for automated task')
    parser.add_argument('-s', '--settings-file', default='settings.json', metavar='FILENAME',
                        help='file to load settings from')
    parser.add_argument('-p', '--private-file', default='private.json', metavar='FILENAME',
                        help='file to save ID and password')
    parser.add_argument('-F', '--force', action='store_true',
                        help='upload even if already uploaded or overdue')
    parser.add_argument('--no-check', action='store_true',
                        help="don't perform js script check")
    parser.add_argument('--no-save', action='store_true',
                        help="don't save ID and password")
    return parser.parse_args()


def load_settings(settings_file='settings.json', private_file='private.json', no_save=False):
    global SETTINGS, URLs
    with open(settings_file, encoding='utf-8') as f:
        SETTINGS = json.load(f)
        URLs = SETTINGS['urls']
    try:
        with open(private_file, encoding='utf-8') as f:
            private = json.load(f)
    except FileNotFoundError:
        private = {'userName': input('学号: '),
                   'password': getpass('密码: ')}
        if not no_save:
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
    session.get(URLs['app_logout'])
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


def get_today_upload_data(session, force=False):
    resp = session.get(URLs['app_entry'])
    session.get(URLs['app_logout'])
    data = SETTINGS['upload_data']
    json = session.get(URLs['app_info']).json()
    for k in data.keys():
        if json['zrtbxx'].get(k):
            data[k] = json['zrtbxx'][k]
    data['tbrq'] = date.today().strftime('%Y%m%d')  # important
    if not force and json.get('mrtbxx'):
        print("Today's report has been submitted earlier.")
        exit(0)
    elif not force and json.get('tbcs') == 'y':
        print("Please complete the report before 13:00 next time.")
        exit(-1)
    else:
        country = json['zrtbxx'].get('dqszdgbm')
        data['dqszdgbm'] = '' if country == '156' else country
    return data


def upload(session, skip_confirm=False, force=False):
    data = get_today_upload_data(session, force)
    if 'required' in data.values():
        pprint(data)
        print('Some of the "required" items are not filled. ' +
              'Please fill and save the form manually for once and/or modify settings.')
    else:
        if not skip_confirm:
            print('The following data will be uploaded:')
            pprint(data)
            ins = input('Confirm? [y]|n:').strip().lower()
        if skip_confirm or ins == '' or ins[0] == 'y':
            json = session.post(URLs['app_post'], data).json()
            assert json['success'], 'SUBMISSION FAILURE: ' + \
                json.get('msg', 'no msg')
            print('Successfully uploaded.')
        else:
            print('Aborted.')


if __name__ == "__main__":
    args = parse_arguments()
    load_settings(args.settings_file, args.private_file, args.no_save)
    session = get_session()
    if not args.confirm:
        print('Loading...')
    login(session)
    if not args.no_check:
        update_check(session)
    upload(session, args.confirm, args.force)
    if not args.confirm:
        input('Press ENTER to exit...')
