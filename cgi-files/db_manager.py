#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""."""

import cgi
import sys
import sqlite3

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
COLUMN_USERNAME = 'username'
COLUMN_PASSWORD = 'password'
COLUMN_EMAIL = 'e_mail'


def output(content):
    """."""
    sys.stdout.write('Content-Type: text/plain\n\n')
    sys.stdout.write(content)


def create_verbs_table():
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_VERBS +
                   ' (' + COLUMN_ID +
                   ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                   COLUMN_INFITIVE + ' TEXT NOT NULL, ' +
                   COLUMN_PRESENT + ' TEXT NOT NULL, ' +
                   COLUMN_PAST + ' TEXT NOT NULL, ' +
                   COLUMN_PRESENT_PERFECT + ' TEXT NOT NULL, ' +
                   COLUMN_INFITIVE_ENGLISH + ' TEXT NOT NULL, ' +
                   COLUMN_TIMES_ASKED + ' TEXT, ' +
                   COLUMN_TIMES_RIGHT + ' TEXT)')

        output('Table "' + TABLE_VERBS + '" created!')
    except Exception as e:
        output('Table "' + TABLE_VERBS + '" NOT created. ' +
               'Exception {}'.format(e))


def create_nouns_table():
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_NOUNS +
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

        output('Table "' + TABLE_NOUNS + '" created!')
    except Exception as e:
        output('Table "' + TABLE_NOUNS + '" NOT created. ' +
               'Exception {}'.format(e))


def create_users_table():
    """."""
    try:
        db.execute('CREATE TABLE IF NOT EXISTS ' + TABLE_USERS +
                   ' (' + COLUMN_ID +
                   ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                   COLUMN_USERNAME + ' TEXT NOT NULL, ' +
                   COLUMN_PASSWORD + ' TEXT NOT NULL, ' +
                   COLUMN_EMAIL + ' TEXT NOT NULL)')

        output('Table "' + TABLE_USERS + '" created!')
    except Exception as e:
        output('Table "' + TABLE_USERS + '" NOT created. ' +
               'Exception {}'.format(e))


def insert_user(username, password, e_mail):
    """."""
    params = (username, password, e_mail)
    try:
        if check_username_availability(username) is True:
            db.execute('INSERT INTO ' + TABLE_USERS + ' (' +
                       COLUMN_USERNAME + ', ' +
                       COLUMN_PASSWORD + ', ' +
                       COLUMN_EMAIL + ') ' +
                       ' VALUES (?,?,?)',
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
    except:
        output('Cannot check username availability')
        return None

form = cgi.FieldStorage()
# output('form {}'.format(form))
db_path = '/var/www/html/languages/database/danish.db'
db = sqlite3.connect(db_path)
cursor = db.cursor()

# insert_user('edu', 'e11235813', 'e.ponzs@gmail.com')

try:
    if 'create table' in form:
        table_name = str(form['create table'].value)

        if table_name == 'verbs':
            create_verbs_table()
        elif table_name == 'nouns':
            create_nouns_table()
        elif table_name == 'users':
            create_users_table()

    elif 'insert' in form:
        table_name = str(form['insert'].value)

        if table_name == 'users':
            username = str(form['username'].value)
            password = str(form['password'].value)
            e_mail = str(form['email'].value)
            insert_user(username, password, e_mail)
except:
    pass

raise SystemExit
