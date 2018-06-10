"""."""

import logging
import os
import sqlite3
import uuid

# from datetime import datetime


class DatabaseManager():
    """
    Class for database management.

    Handles the creation of 4 tables.
    Provides the methods necessary to operate them.
    """

    # *********************** GENERAL *********************** #

    def __init__(self):
        """
        Contructor.

        Initializes table and column names.
        Connects to the database.
        Creates the tables if they do not exist.
        """
        self.logger = logging.getLogger('rest_api.database_lib')
        self.logger.setLevel(logging.INFO)

        self.TABLE_VERBS = 'verbs'
        self.COLUMN_ID = 'id'
        self.COLUMN_INFITIVE = 'infinitive'
        self.COLUMN_PRESENT = 'present'
        self.COLUMN_PAST = 'past'
        self.COLUMN_PRESENT_PERFECT = 'present_perfect'
        self.COLUMN_INFITIVE_ENGLISH = 'infinitive_english'
        self.COLUMN_TOPIC = 'topic'
        self.COLUMN_TIMES_ASKED = 'times_asked'
        self.COLUMN_TIMES_RIGHT = 'times_right'

        self.TABLE_NOUNS = 'nouns'
        self.COLUMN_DEF_DAN = 'define_form'
        self.COLUMN_DEF_ENG = 'define_form_english'
        self.COLUMN_UNDEF_DAN = 'undefine_form'
        self.COLUMN_UNDEF_ENG = 'undefine_form_english'
        self.COLUMN_PLURAL_DAN = 'plural'
        self.COLUMN_PLURAL_ENG = 'plural_english'
        self.COLUMN_PLURAL_DEF_DAN = 'plural_define'
        self.COLUMN_PLURAL_DEF_ENG = 'plural_define_english'

        self.TABLE_USERS = 'users'
        self.COLUMN_USER_ID = 'user_id'
        self.COLUMN_USERNAME = 'username'
        self.COLUMN_PASSWORD = 'password'
        self.COLUMN_EMAIL = 'e_mail'

        db_path = '/var/www/html/languages/application/database/danish.db'
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

        self.logger.debug('Connecting to database.' +
                          ' Database path: {}'.format(db_path))
        self.db = sqlite3.connect(db_path)
        os.chmod(db_path, 0o777)

        self.create_users_table()
        self.create_verbs_table()

    # *********************** USERS *********************** #
    def create_users_table(self):
        """."""
        try:
            self.db.execute('CREATE TABLE IF NOT EXISTS ' + self.TABLE_USERS +
                            ' (' + self.COLUMN_ID +
                            ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                            self.COLUMN_USER_ID + ' TEXT NOT NULL, ' +
                            self.COLUMN_USERNAME + ' TEXT NOT NULL, ' +
                            self.COLUMN_PASSWORD + ' TEXT NOT NULL, ' +
                            self.COLUMN_EMAIL + ' TEXT NOT NULL)')

            return True
        except Exception as e:
            self.logger.warning('Table {} NOT created. Exception {}'.format(self.TABLE_USERS, e))
            return False

    def insert_user(self, username, password, e_mail):
        """."""
        user_id = str(uuid.uuid4())
        user_id = user_id.replace("-", "")
        params = (user_id, username, password, e_mail)
        try:
            if self.check_username_availability(username) is True:
                self.db.execute('INSERT INTO ' + self.TABLE_USERS + ' (' +
                                self.COLUMN_USER_ID + ', ' +
                                self.COLUMN_USERNAME + ', ' +
                                self.COLUMN_PASSWORD + ', ' +
                                self.COLUMN_EMAIL + ') ' +
                                ' VALUES (?,?,?,?)',
                                params)
                self.db.commit()
                return 'New user inserted in the database'
            else:
                return 'User already exists'
        except Exception as e:
            self.logger.info('Cannot insert user. Exception {}'.format(e))
            return 'Cannot insert user.'

    def check_username_availability(self, username):
        """."""
        try:
            self.cursor.execute('SELECT ' + self.COLUMN_USERNAME +
                                ' FROM ' + self.TABLE_USERS +
                                ' WHERE ' + self.COLUMN_USERNAME + ' = "' + username + '"')
            if len(self.cursor.fetchall()) > 0:
                return False
            else:
                return True
        except Exception as e:
            self.logger.warning('Cannot check username availability. Exception {}'.format(e))
            return None

    def get_user_id(self, username, password):
        """."""
        try:
            self.cursor.execute('SELECT ' + self.COLUMN_USER_ID +
                                ' FROM ' + self.TABLE_USERS +
                                ' WHERE ' + self.COLUMN_USERNAME + ' = "' + str(username) +
                                '" AND ' + self.COLUMN_PASSWORD + ' = "' + str(password) + '"')

            row = self.cursor.fetchone()

            if row is not None:
                user_id = row[0]
            else:
                user_id = 0

            return user_id

        except Exception as e:
            self.logger.warning('Cannot get user id. Exception {}'.format(e))
            return 0

    def check_login(self, username, password):
        """."""
        try:
            self.cursor.execute('SELECT ' +
                                self.COLUMN_USERNAME + ', ' +
                                self.COLUMN_PASSWORD +
                                ' FROM ' + self.TABLE_USERS +
                                ' WHERE ' + self.COLUMN_USERNAME + ' = "' + username +
                                '" AND ' + self.COLUMN_PASSWORD + ' = "' + password + '"')
            if len(self.cursor.fetchall()) > 0:
                return True
            else:
                return False
        except Exception as e:
            self.logger.info('Cannot check login. Exception {}'.format(e))
            return False

    def update_user(self, username, password, new_username, new_password, new_email):
        """."""
        user_id = self.get_user_id(username, password) if self.check_login(username, password) else ''

        if user_id:
            params = (new_username, new_password, new_email, user_id)
            try:
                self.cursor.execute('UPDATE ' + self.TABLE_USERS +
                                    ' SET ' +
                                    self.COLUMN_USERNAME + ' = ?, ' +
                                    self.COLUMN_PASSWORD + ' = ?, ' +
                                    self.COLUMN_EMAIL + ' = ?' +
                                    ' WHERE ' + self.COLUMN_USER_ID + ' = ?',
                                    params)
                self.db.commit()
                count = self.cursor.rowcount
                if count > 0:
                    self.logger.info('rows updated {}'.format(count))
                return 'User updated'
            except Exception as e:
                self.logger.warning('Cannot update user. Exception {}'.format(e))
                return 'Cannot update user'
        else:
            return 'Incorrect username or password'

    # *********************** VERBS *********************** #
    def create_verbs_table(self):
        """."""
        try:
            self.db.execute('CREATE TABLE IF NOT EXISTS ' + self.TABLE_VERBS +
                            ' (' + self.COLUMN_ID +
                            ' INTEGER PRIMARY KEY AUTOINCREMENT, ' +
                            self.COLUMN_INFITIVE + ' TEXT NOT NULL, ' +
                            self.COLUMN_PRESENT + ' TEXT NOT NULL, ' +
                            self.COLUMN_PAST + ' TEXT NOT NULL, ' +
                            self.COLUMN_PRESENT_PERFECT + ' TEXT NOT NULL, ' +
                            self.COLUMN_INFITIVE_ENGLISH + ' TEXT NOT NULL, ' +
                            self.COLUMN_TOPIC + ' TEXT NOT NULL, ' +
                            self.COLUMN_TIMES_ASKED + ' TEXT, ' +
                            self.COLUMN_TIMES_RIGHT + ' TEXT)')

            return True
        except Exception as e:
            self.logger.warning('Table {} NOT created. Exception {}'.format(self.TABLE_VERBS, e))
            return False

    def check_verb_availability(self, infinitive):
        """."""
        try:
            self.cursor.execute('SELECT ' + self.COLUMN_INFITIVE +
                                ' FROM ' + self.TABLE_VERBS +
                                ' WHERE ' + self.COLUMN_INFITIVE + ' = "' + infinitive + '"')
            if len(self.cursor.fetchall()) > 0:
                return False
            else:
                return True
        except Exception as e:
            self.logger.warning('Cannot check verb availability. Exception {}'.format(e))
            return None

    def insert_verb(self, infinitive, present, past, present_perfect, infinitive_eng, topic):
        """."""
        if self.check_verb_availability(infinitive):
            params = (infinitive, present, past, present_perfect, infinitive_eng, topic)
            try:
                # self.logger.info('insert_verb() 2')
                self.db.execute('INSERT INTO ' + self.TABLE_VERBS + ' (' +
                                self.COLUMN_INFITIVE + ', ' +
                                self.COLUMN_PRESENT + ', ' +
                                self.COLUMN_PAST + ', ' +
                                self.COLUMN_PRESENT_PERFECT + ', ' +
                                self.COLUMN_INFITIVE_ENGLISH + ', ' +
                                self.COLUMN_TOPIC + ') ' +
                                ' VALUES (?,?,?,?,?,?)',
                                params)
                self.db.commit()
                return 'Verb inserted in the database'
            except Exception as e:
                self.logger.warning('Cannot insert user. Exception {}'.format(e))
                return 'Cannot insert verb'
        else:
            return 'Verb already exists'

    def update_verb(self, infinitive, new_infinitive, new_present, new_past,
                    new_present_perfect, new_infinitive_eng):
        """."""
        if not self.check_verb_availability(infinitive):
            params = (new_infinitive, new_present, new_past, new_present_perfect,
                      new_infinitive_eng, infinitive)
            try:
                self.cursor.execute('UPDATE ' + self.TABLE_VERBS +
                                    ' SET ' +
                                    self.COLUMN_INFITIVE + ' = ?, ' +
                                    self.COLUMN_PRESENT + ' = ?, ' +
                                    self.COLUMN_PAST + ' = ?,' +
                                    self.COLUMN_PRESENT_PERFECT + ' = ?, ' +
                                    self.COLUMN_INFITIVE_ENGLISH + ' = ? ' +
                                    ' WHERE ' + self.COLUMN_INFITIVE + ' = ?',
                                    params)
                self.db.commit()
                count = self.cursor.rowcount
                if count > 0:
                    self.logger.info('rows updated {}'.format(count))
                return 'Verb updated'
            except Exception as e:
                self.logger.warning('Cannot update verb. Exception {}'.format(e))
                return 'Cannot update verb'
        else:
            return 'The verb does not exist on the database'
