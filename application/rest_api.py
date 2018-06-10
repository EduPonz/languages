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

app = Flask(__name__)
FlaskUUID(app)
CORS(app)


@app.route('/test', methods=['POST'])
def post_test():
    """."""
    print('Post request {}'.format(request.json))
    logger.info('Post request {}'.format(request.json))
    return jsonify({'test': 'return message'}), 201


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

    print('\n\n\n\n\n{:{fill}{align}{width}}\n'.format(' APLICATION START ', fill='*', align='^', width=130))
    logger.info('\n\n\n\n\n{:{fill}{align}{width}}\n'.format(' APLICATION START ', fill='*',
                                                             align='^', width=130))

    app.run(debug=False, host='0.0.0.0')
