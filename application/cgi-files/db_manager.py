#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""."""

import cgi
import logging
import sys
import sqlite3
import uuid
from logging.handlers import RotatingFileHandler

TABLE_VERBS = 'verbs'
COLUMN_ID = 'id'
COLUMN_INFITIVE = 'infinitive'
COLUMN_PRESENT = 'present'
COLUMN_PAST = 'past'
COLUMN_PRESENT_PERFECT = 'present_perfect'
COLUMN_INFITIVE_ENGLISH = 'infinitive_english'
COLUMN_TOPIC = 'topic'
COLUMN_TIMES_ASKED = 'times_asked'
COLUMN_TIMES_RIGHT = 'times_right'

TABLE_NOUNS = 'nouns'
COLUMN_DEF_DAN = 'define_form'
COLUMN_DEF_ENG = 'define_form_english'
COLUMN_UNDEF_DAN = 'undefine_form'
COLUMN_UNDEF_ENG = 'undefine_form_english'
COLUMN_PLURAL_DAN = 'plural'
COLUMN_PLURAL_ENG = 'plural_english'
COLUMN_PLURAL_DEF_DAN = 'plural_define'
COLUMN_PLURAL_DEF_ENG = 'plural_define_english'

TABLE_USERS = 'users'
COLUMN_USER_ID = 'user_id'
COLUMN_USERNAME = 'username'
COLUMN_PASSWORD = 'password'
COLUMN_EMAIL = 'e_mail'

log_location = '/var/www/html/languages/application/log/db_manager.log'
logger = logging.getLogger('db_manager')
handler = RotatingFileHandler(log_location, maxBytes=200000,
                              backupCount=10)
formatter = logging.Formatter('[%(asctime)s][%(name)s]' +
                              '[%(levelname)s] %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def output(content):
    """."""
    sys.stdout.write('Content-Type: text/plain\n\n')
    sys.stdout.write(content)


def create_verbs_table(table_name):
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                   ' (' + COLUMN_ID +
                   ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                   COLUMN_INFITIVE + ' TEXT NOT NULL, ' +
                   COLUMN_PRESENT + ' TEXT NOT NULL, ' +
                   COLUMN_PAST + ' TEXT NOT NULL, ' +
                   COLUMN_PRESENT_PERFECT + ' TEXT NOT NULL, ' +
                   COLUMN_INFITIVE_ENGLISH + ' TEXT NOT NULL, ' +
                   COLUMN_TOPIC + ' TEXT NOT NULL, ' +
                   COLUMN_TIMES_ASKED + ' TEXT, ' +
                   COLUMN_TIMES_RIGHT + ' TEXT)')

        return True
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))
        return False


def create_nouns_table(table_name):
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                   ' (' + COLUMN_ID +
                   ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                   COLUMN_DEF_DAN + ' TEXT NOT NULL, ' +
                   COLUMN_DEF_ENG + ' TEXT NOT NULL, ' +
                   COLUMN_UNDEF_DAN + ' TEXT NOT NULL, ' +
                   COLUMN_UNDEF_ENG + ' TEXT NOT NULL, ' +
                   COLUMN_PLURAL_DAN + ' TEXT NOT NULL, ' +
                   COLUMN_PLURAL_ENG + ' TEXT NOT NULL, ' +
                   COLUMN_PLURAL_DEF_DAN + ' TEXT NOT NULL, ' +
                   COLUMN_PLURAL_DEF_ENG + ' TEXT NOT NULL, ' +
                   COLUMN_TOPIC + ' TEXT NOT NULL, ' +
                   COLUMN_TIMES_ASKED + ' TEXT, ' +
                   COLUMN_TIMES_RIGHT + ' TEXT)')

        return True
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))
        return False


def create_users_table(table_name):
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                   ' (' + COLUMN_ID +
                   ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                   COLUMN_USER_ID + ' TEXT NOT NULL, ' +
                   COLUMN_USERNAME + ' TEXT NOT NULL, ' +
                   COLUMN_PASSWORD + ' TEXT NOT NULL, ' +
                   COLUMN_EMAIL + ' TEXT NOT NULL)')

        return True
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))
        return False


def insert_user(username, password, e_mail):
    """."""
    user_id = str(uuid.uuid4())
    user_id = user_id.replace("-", "")
    params = (user_id, username, password, e_mail)
    try:
        if check_username_availability(username) is True:
            db.execute('INSERT INTO ' + TABLE_USERS + ' (' +
                       COLUMN_USER_ID + ', ' +
                       COLUMN_USERNAME + ', ' +
                       COLUMN_PASSWORD + ', ' +
                       COLUMN_EMAIL + ') ' +
                       ' VALUES (?,?,?,?)',
                       params)

            db.commit()
            return True
        else:
            return False
    except Exception as e:
        output('Cannot insert user. Exception {}'.format(e))
        return False


def check_username_availability(username):
    """."""
    try:
        cursor.execute('SELECT ' + COLUMN_USERNAME +
                       ' FROM ' + TABLE_USERS +
                       ' WHERE ' + COLUMN_USERNAME + ' = "' + username + '"')
        if len(cursor.fetchall()) > 0:
            return False
        else:
            return True
    except Exception as e:
        output('Cannot check username availability. Exception {}'.format(e))
        return None


def check_login(username, password):
    """."""
    try:
        cursor.execute('SELECT ' +
                       COLUMN_USERNAME + ', ' +
                       COLUMN_PASSWORD +
                       ' FROM ' + TABLE_USERS +
                       ' WHERE ' + COLUMN_USERNAME + ' = "' + username +
                       '" AND ' + COLUMN_PASSWORD + ' = "' + password + '"')
        if len(cursor.fetchall()) > 0:
            return True
        else:
            return False
    except Exception as e:
        output('Cannot check login. Exception {}'.format(e))
        return False


def get_user_id(username):
    """."""
    try:
        cursor.execute('SELECT ' + COLUMN_USER_ID +
                       ' FROM ' + TABLE_USERS +
                       ' WHERE ' + COLUMN_USERNAME + ' = "' + username + '"')

        user_id = cursor.fetchone()[0]
        return user_id

    except Exception as e:
        output('Cannot get user id. Exception {}'.format(e))


def update_user(user_id, new_username, new_password, new_email):
    """."""
    params = (new_username, new_password, new_email, user_id)
    try:
        cursor.execute('UPDATE ' + TABLE_USERS +
                       ' SET ' +
                       COLUMN_USERNAME + ' = ?, ' +
                       COLUMN_PASSWORD + ' = ?, ' +
                       COLUMN_EMAIL + ' = ?' +
                       ' WHERE ' + COLUMN_USER_ID + ' = ?',
                       params)
        db.commit()
        return True
    except Exception as e:
        output('Cannot update user. Exception {}'.format(e))
        return False


def insert_verb(infinitive, infinitive_eng, present, past,
                present_perfect):
    """."""
    output('insert_verb() 1')
    params = (infinitive, infinitive_eng, present, past,
              present_perfect)
    try:
        output('insert_verb() 2')
        db.execute('INSERT INTO ' + TABLE_VERBS + ' (' +
                   COLUMN_INFITIVE + ', ' +
                   COLUMN_PRESENT + ', ' +
                   COLUMN_PAST + ', ' +
                   COLUMN_PRESENT_PERFECT + ', ' +
                   COLUMN_INFITIVE_ENGLISH + ') ' +
                   ' VALUES (?,?,?,?,?)',
                   params)
        output('insert_verb() 3')
        db.commit()
        output('insert_verb() 4')
        return True
    except Exception as e:
        output('insert_verb() 5')
        output('Cannot insert user. Exception {}'.format(e))
        return False


form = cgi.FieldStorage()
logger.info('form {}'.format(form))
output('form {}'.format(form))
db_path = '/var/www/html/languages/application/database/danish.db'
db = sqlite3.connect(db_path)
cursor = db.cursor()

try:
    if 'create table' in form:
        table_name = str(form['create table'].value)

        if table_name == 'verbs':
            if create_verbs_table(table_name):
                output('Table "' + table_name + '" created!')
        elif table_name == 'nouns':
            if create_nouns_table(table_name):
                output('Table "' + table_name + '" created!')
        elif table_name == 'users':
            if create_users_table(table_name):
                output('Table "' + table_name + '" created!')

    elif 'insert' in form:
        table_name = str(form['insert'].value)

        if table_name == 'users':
            username = str(form['username'].value)
            password = str(form['password'].value)
            e_mail = str(form['email'].value)
            if insert_user(username, password, e_mail):
                output('User inserted!')
            else:
                output('User already exists!')

    elif 'login' in form:

        username = str(form['username'].value)
        password = str(form['password'].value)

        if check_login(username, password):
            user_id = get_user_id(username)
            append_name = '_' + user_id
            table_verbs = TABLE_VERBS + append_name
            table_nouns = TABLE_NOUNS + append_name

            create_verbs_table(table_verbs)
            create_nouns_table(table_nouns)

            output('login correct')
        else:
            output('login NOT correct')

    elif 'update_user' in form:
        username = str(form['username'].value)
        password = str(form['password'].value)

        if check_login(username, password):
            user_id = get_user_id(username)
            new_username = str(form['new_username'].value)
            new_password = str(form['new_password'].value)
            new_email = str(form['new_email'].value)
            if update_user(user_id, new_username, new_password, new_email):
                output('User updated!')
            else:
                output('User NOT updated!')

    elif 'insert_verb' in form:
        output('insert_verb 1')
        output('form {}'.format(form['insert_verb']))
        infinitive_eng = str(form['insert_verb'].value)
        output(infinitive_eng)
        infinitive = str(form['verb_infinitive'].value)
        output(infinitive)
        present = str(form['verb_present'].value)
        output(present)
        past = str(form['verb_past'].value)
        output(past)
        present_perfect = str(form['verb_present_perf'].value)
        output(present_perfect)

        if (insert_verb(infinitive, infinitive_eng, present, past,
                        present_perfect) is True):
            output('insert_verb 2')
            output('Verb inserted')
        else:
            output('insert_verb 3')
            output('Verb NOT inserted')

except:
    pass

raise SystemExit
