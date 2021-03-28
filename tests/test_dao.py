import sqlite3
import tempfile
import uuid

import pytest

from relocation_helper.appConfig import ApplicationConfiguration
from relocation_helper.dao import Dao
from relocation_helper.migration import Migration

config = ApplicationConfiguration()
config.basePath = tempfile.gettempdir() + "/relocation_helper_%s.db" % uuid.uuid4()

migration = Migration(config)
migration.migrate()
dao = Dao(config)


def test_insert_box():
    dao.addBox("zzz")
    assert dao.isBoxExists("zzz") == True
    assert dao.getBoxId("zzz") == 1


def test_unique_key():
    with pytest.raises(sqlite3.IntegrityError):
        dao.addBox("zzz_kkk")
        dao.addBox("zzz_kkk")
