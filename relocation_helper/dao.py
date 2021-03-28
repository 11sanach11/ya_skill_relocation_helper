import logging
import sqlite3

from relocation_helper.appConfig import ApplicationConfiguration


class Dao:

    def __init__(self, config: ApplicationConfiguration):
        self.daoLog = logging.getLogger("dao")
        self.con = sqlite3.connect(config.basePath, check_same_thread=False)

    def getBoxId(self, boxName: str):
        cur = self.con.cursor()
        cur.execute("SELECT id FROM boxes WHERE box_name=?", (boxName,))
        rez = cur.fetchone()
        self.con.commit()
        cur.close()
        return rez[0] if rez else None

    def isBoxExists(self, boxName: str):
        cur = self.con.cursor()
        cur.execute("SELECT count(id) FROM boxes WHERE box_name=?", (boxName,))
        rez = cur.fetchone()
        self.con.commit()
        cur.close()
        return rez[0] == 1

    def addBox(self, boxName: str):
        cur = self.con.cursor()
        cur.execute("INSERT INTO boxes (box_name) VALUES (?)", (boxName,))
        self.con.commit()
        cur.close()

    def addItemIntoBox(self, boxId: int, item: str):
        cur = self.con.cursor()
        cur.execute("INSERT INTO items (item_name,box_id) VALUES (?,?)", (item, boxId))
        self.con.commit()
        cur.close()

    def __del__(self):
        self.con.close()
