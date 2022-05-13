import sqlite3


class DatabaseControl:
    def __init__(self):
        try:
            self.sqlite_connection = sqlite3.connect('users.db',
                                                     check_same_thread=False)
            sqlite_create_table_query = '''CREATE TABLE bot_users (
                                        uid INTEGER PRIMARY KEY,
                                        plan TEXT,
                                        codes_left INTEGER);'''
            cursor = self.sqlite_connection.cursor()
            cursor.execute(sqlite_create_table_query)
            self.sqlite_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("ERROR:  ", error)

    def __del__(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()

    def add_user(self, uid, plan, left):
        sqlite_add = '''INSERT INTO bot_users (uid, plan, codes_left)
                    VALUES({}, "{}", {});'''
        sqlite_add = sqlite_add.format(uid, plan, left)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_add)
        self.sqlite_connection.commit()
        cursor.close()

    def change_codes_left(self, uid, delta):
        c = 'UPDATE bot_users SET codes_left = codes_left + {} WHERE uid = {};'
        sqlite_change = c.format(delta, uid)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_change)
        self.sqlite_connection.commit()
        cursor.close()

    def get_plan(self, uid):
        sqlite_change = 'SELECT plan FROM bot_users WHERE uid = {}'.format(uid)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_change)
        self.sqlite_connection.commit()
        res = cursor.fetchone()
        cursor.close()
        return res[0]

    def get_codes_left(self, uid):
        c = 'SELECT codes_left FROM bot_users WHERE uid = {}'
        sqlite_change = c.format(uid)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_change)
        self.sqlite_connection.commit()
        res = cursor.fetchone()
        cursor.close()
        return int(res[0])

    def set_plan(self, uid, plan):
        c = 'UPDATE bot_users SET plan = "{}" WHERE uid = {};'
        sqlite_change = c.format(plan, uid)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_change)
        self.sqlite_connection.commit()
        cursor.close()

    def check_uid(self, uid):
        c = 'SELECT EXISTS (SELECT 1 FROM bot_users WHERE uid = {} )'
        sqlite_change = c.format(uid)
        cursor = self.sqlite_connection.cursor()
        cursor.execute(sqlite_change)
        self.sqlite_connection.commit()
        res = cursor.fetchone()
        cursor.close()
        return bool(res[0])

