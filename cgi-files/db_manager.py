#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""."""

import cgi
import sys
import sqlite3


def output(content):
    """."""
    sys.stdout.write('Content-Type: text/plain\n\n')
    sys.stdout.write(content)

form = cgi.FieldStorage()

db_path = '/var/www/html/languages/database/danish.db'

db = sqlite3.connect(db_path)
cursor = db.cursor()

try:
    if 'create table' in form:
        table_name = str(form['create table'].value)
        try:
            db.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                       ' (id INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                       'infinitive TEXT NOT NULL, ' +
                       'infinitive_english TEXT NOT NULL)')
            output('Table, ' + table_name + ' created!')
        except Exception as e:
            output('Table, ' + table_name + ' NOT created. ' +
                   'Exception {}'.format(e))
except:
    pass

raise SystemExit
