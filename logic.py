#! python3
# -*- coding: utf-8 -*-
import db_utils
from utils import list_db


class Logic(object):
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = list_db()[0]

        self.db_connector = db_utils.DbDaemon('main.db', db_path)
        self.db_connector.connect()
        self.my_name = self.set_my_name()

    def set_my_name(self):
        query = """
            SELECT skypename
            FROM "Accounts"
        """
        return self.db_connector.execute(query, (), fetchone=True)[0]
    
    def find_contact(self, search_string):
        query = """
            SELECT id, skypename, fullname
            FROM "Contacts"
            WHERE
              fullname LIKE ?
            OR
              skypename LIKE ?
            ORDER BY id
        """
        search_string = '%' + search_string + '%'
        data = self.db_connector.execute(query, (search_string, search_string))
        return data

    def list_contacts(self):
        query = """
            SELECT id, skypename, fullname
            FROM "Contacts"
            ORDER BY id
        """
        data = self.db_connector.execute(query, ())
        return data

    def get_messages(self, skype_name, time_start=None, time_end=None, limit=None):
        """
            :param skype_name - string
            :param time_start - sql compatible string ('yyyy-mm--dd')
            :param time_end - sql compatible string ('yyyy-mm--dd')
            :param limit - int
        """
        query = """
            SELECT id,
                datetime("Messages".timestamp, 'unixepoch', 'localtime') as time_stamp,
                 from_dispname as author,
                 author = :my_name as is_mine,
                  body_xml as msg_text
            FROM "Messages"
            WHERE "Messages".convo_id = :convo_id
              AND (:time_start is NULL OR "Messages".timestamp > strftime( '%s', :time_start))
              AND (:time_end is NULL OR "Messages".timestamp < strftime( '%s', :time_end))
            ORDER BY id ASC
        """
        if limit is not None:
            query += """\nLIMIT :limit\n"""
        params = {
            'my_name': self.my_name,
            'time_start': time_start,
            'time_end': time_end,
            'convo_id': self._get_convo_id_by_name(skype_name),
            'limit': limit
        }
        return self.db_connector.execute(query, params)

    def _get_convo_id_by_name(self, skype_name):
        query = """
            SELECT id FROM "Conversations" WHERE identity LIKE ?
        """
        params = ('%' + skype_name + '%',)
        identifier = self.db_connector.execute(query, params, fetchone=True)
        return identifier[0] if identifier is not None else False
