import logging
import sqlite3
import threading
from sqlite3.dbapi2 import Cursor

from relocation_helper.appConfig import ApplicationConfiguration


class Dao:

    def _safeExecution(func):
        def wrapper(self, *args, **kwargs):
            with self._assignLock:
                cur = self.con.cursor()
                rez = (func(self, *args, **kwargs))(cur)
                self.con.commit()
                cur.close()
                return rez

        return wrapper

    def __init__(self, config: ApplicationConfiguration):
        self.daoLog = logging.getLogger("dao")
        self.con = sqlite3.connect(config.basePath, check_same_thread=False)
        self._assignLock = threading.Lock()

    @_safeExecution
    def getBoxId(self, boxName: str):
        def cursor(cur: Cursor):
            cur.execute("SELECT id FROM boxes WHERE box_name=?", (boxName,))
            rez = cur.fetchone()
            return rez[0] if rez else None

        return cursor

    @_safeExecution
    def isBoxExists(self, boxName: str):
        def cursor(cur: Cursor):
            cur.execute("SELECT count(id) FROM boxes WHERE box_name=?", (boxName,))
            return cur.fetchone()[0] == 1

        return cursor

    @_safeExecution
    def addBox(self, boxName: str):
        def cursor(cur: Cursor):
            return cur.execute("INSERT INTO boxes (box_name) VALUES (?)", (boxName,))

        return cursor

    @_safeExecution
    def addItemIntoBox(self, boxId: int, item: str):
        def cursor(cur: Cursor):
            return cur.execute("INSERT INTO items (item_name,box_id) VALUES (?,?)", (item, boxId))

        return cursor

    def __del__(self):
        self.con.close()
