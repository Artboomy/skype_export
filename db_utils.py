#! python3
# -*- coding: utf-8 -*-
import sqlite3
from utils import logger_init


class DbDaemon(object):
    _debug = True

    def __init__(self, db_name, db_path=None, logger=None):
        if db_path is not None:
            # hax if path contains db name
            full_db_name = db_path.replace(db_name, '') + db_name
        else:
            full_db_name = db_name

        if logger is None:
            logger = logger_init('DB_log')

        self.logger = logger
        self.db_name = db_name
        # full name - with path
        self._full_db_name = full_db_name
        self._db_connector = None

    def connect(self):
        try:
            self._db_connector = sqlite3.connect(self._full_db_name)
            # for convenient access to result fields as dict attributes
            self._db_connector.row_factory = sqlite3.Row
            self.logger.info('Successfully connected to ' + self._full_db_name)
        except sqlite3.Error as e:
            self.logger.error('Connection error: "{0}"'.format(e.args[0]))

    def disconnect(self):
        try:
            self._db_connector.close()
            self.logger.info('Connection to {0} closed successfully'.format(self.db_name))
        except sqlite3.Error as e:
            self.logger.error('Disconnection error: ' + e.args[0])

    def _log_error(self, error, command, no_raise=False):
        self.logger.error('Execution error: "{0}", trying to execute command: "{1}"'.format(error.args[0], command))
        if no_raise is False:
            raise error

    def execute(self, command, params, fetchone=False):
        cursor = self._db_connector.cursor()
        try:
            if self._debug:
                self.logger.info('Executing command {0} with params {1}'.format(command, str(params)))
            cursor.execute(command, params)
            result = cursor.fetchall() if fetchone is False else cursor.fetchone()
            return result
        except sqlite3.Error as e:
            self._log_error(e, command)
