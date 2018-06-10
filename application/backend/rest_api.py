"""
REST API.

Script receiving GET, POST and PUT requests from both a socket and a UI.
Created by Sigitas Dagilis for Seluxit. 10-nov-2017.
"""

# !/usr/bin/python3

import logging
import os
# import uuid
import time
# import json
from flask_uuid import FlaskUUID
from flask_cors import CORS
from flask import Flask, jsonify, request  # , make_response, request, abort
from logging.handlers import RotatingFileHandler
from database_lib import DatabaseManager

app = Flask(__name__)
FlaskUUID(app)
CORS(app)


@app.route('/insert-user', methods=['POST'])
def insert_user():
    """."""
    print('Post request {}'.format(request.json))
    logger.info('Post request {}'.format(request.json))

    data = request.json['data'] if request.json['type'] == 'insert_user' else ''
    if data:
        result = db.insert_user(data['username'], data['password'], data['email'])
    return jsonify({'data': result}), 201


@app.route('/check-login', methods=['POST'])
def check_login():
    """."""
    print('Post request {}'.format(request.json))
    logger.info('Post request {}'.format(request.json))

    data = request.json['data'] if request.json['type'] == 'check_login' else ''
    result = False
    if data:
        result = db.check_login(data['username'], data['password'])
    return jsonify({'data': result}), 201


@app.route('/update-user', methods=['POST'])
def update_user():
    """."""
    print('Post request {}'.format(request.json))
    logger.info('Post request {}'.format(request.json))

    data = request.json['data'] if request.json['type'] == 'update_user' else ''
    if data:
        result = db.update_user(data['username'], data['password'], data['new_username'],
                                data['new_password'], data['new_email'])
    return jsonify({'data': result}), 201


@app.route('/insert-verb', methods=['POST'])
def insert_verb():
    """."""
    print('Post request {}'.format(request.json))
    logger.info('Post request {}'.format(request.json))

    data = request.json['data'] if request.json['type'] == 'insert_verb' else ''
    if data:
        result = db.insert_verb(data['infinitive'], data['present'], data['past'],
                                data['present_perfect'], data['infinitive_eng'])
    return jsonify({'data': result}), 201


# *********************** MAIN *********************** #

if __name__ == '__main__':
    log_location = os.path.dirname(__file__)
    log_location = os.path.abspath(os.path.join(log_location, "log"))
    log_location = os.path.abspath(os.path.join(log_location, "rest_api.log"))

    logger = logging.getLogger('rest_api')
    handler = RotatingFileHandler(log_location, maxBytes=200000,
                                  backupCount=10)
    formatter = logging.Formatter('[%(asctime)s][%(name)s]' +
                                  '[%(levelname)s] %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    time.sleep(1)

    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True

    db = DatabaseManager()

    print('\n\n\n\n\n{:{fill}{align}{width}}\n'.format(' APLICATION START ', fill='*', align='^', width=130))
    logger.info('\n\n\n\n\n{:{fill}{align}{width}}\n'.format(' APLICATION START ', fill='*',
                                                             align='^', width=130))

    app.run(debug=False, host='0.0.0.0')
