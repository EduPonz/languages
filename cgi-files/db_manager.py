#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""."""

import cgi
import sys
import sqlite3
import uuid

TABLE_VERBS = 'verbs'
COLUMN_ID = 'id'
COLUMN_INFITIVE = 'infinitive'
COLUMN_PRESENT = 'present'
COLUMN_PAST = 'past'
COLUMN_PRESENT_PERFECT = 'present_perfect'
COLUMN_INFITIVE_ENGLISH = 'infinitive_english'
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
                   COLUMN_TIMES_ASKED + ' TEXT, ' +
                   COLUMN_TIMES_RIGHT + ' TEXT)')

        output('Table "' + table_name + '" created!')
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))


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
                   COLUMN_TIMES_ASKED + ' TEXT, ' +
                   COLUMN_TIMES_RIGHT + ' TEXT)')

        output('Table "' + table_name + '" created!')
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))


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

        output('Table "' + table_name + '" created!')
    except Exception as e:
        output('Table "' + table_name + '" NOT created. ' +
               'Exception {}'.format(e))


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
            output('User inserted!')
        else:
            output('User already exists!')
    except Exception as e:
        output('Cannot insert user. Exception {}'.format(e))


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
            output('login correct')
            return True
        else:
            output('login not correct')
            return False
    except Exception as e:
        output('Cannot check login. Exception {}'.format(e))
        return None


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
        output('User updated!')
    except Exception as e:
        output('Cannot update user. Exception {}'.format(e))


form = cgi.FieldStorage()
db_path = '/var/www/html/languages/database/danish.db'
db = sqlite3.connect(db_path)
cursor = db.cursor()

try:
    if 'create table' in form:
        table_name = str(form['create table'].value)

        if table_name == 'verbs':
            create_verbs_table(table_name)
        elif table_name == 'nouns':
            create_nouns_table(table_name)
        elif table_name == 'users':
            create_users_table(table_name)

    elif 'insert' in form:
        table_name = str(form['insert'].value)

        if table_name == 'users':
            username = str(form['username'].value)
            password = str(form['password'].value)
            e_mail = str(form['email'].value)
            insert_user(username, password, e_mail)

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

    elif 'update_user' in form:
        username = str(form['username'].value)
        password = str(form['password'].value)

        if check_login(username, password):
            user_id = get_user_id(username)
            new_username = str(form['new_username'].value)
            new_password = str(form['new_password'].value)
            new_email = str(form['new_email'].value)
            update_user(user_id, new_username, new_password, new_email)

except:
    pass

raise SystemExit
