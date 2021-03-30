import tempfile
import uuid

import pytest

from relocation_helper.appConfig import ApplicationConfiguration
from relocation_helper.dao import Dao
from relocation_helper.migration import Migration
from relocation_helper.skillLogic import SkillLogic, YaDRequest, YaDRequestObject, YaDRequestSessionObject

config = ApplicationConfiguration()
config.basePath = tempfile.gettempdir() + "/relocation_helper_%s.db" % uuid.uuid4()

migration = Migration(config)
migration.migrate()
dao = Dao(config)

logic = SkillLogic(config, dao)


def createResponse(command: str):
    return YaDRequest(
        request=YaDRequestObject(
            command=command,
            original_utterance=config,
            nlu=command.split(" ")
        ),
        version="1.0",
        session=YaDRequestSessionObject(
            message_id=10,
            session_id="10",
            new=False
        )
    )


def test_unknown_command():
    resp = logic.process(createResponse("zzz"))
    assert resp.response.text == "Не понимаю, что нужно делать, если нужно помочь с командами, скажи: помоги"


def test_create_box_repeat():
    resp = logic.process(createResponse("создай коробку один"))
    assert resp.response.text == "Коробка один создана, теперь можно помещать в нее вещи"
    resp = logic.process(createResponse("создай коробку один"))
    assert resp.response.text == "Коробка один уже есть, не нужно снова её создавать, можете помещать в неё вещи"

@pytest.mark.parametrize("command",
                         ["положить в коробку 25 предмет банан",
                          "положи в коробку 25 предмет банан",
                          "добавить в коробку 25 предмет банан",
                          "добавь в коробку 25 предмет банан",
                          "поклади коробку 25 предмет банан"])
def test_put_item_into_box(command):
    resp = logic.process(createResponse("положить в коробку 25 предмет банан"))
    assert resp.response.text == "Не могу найти коробку с названием: 25, нужно сперва ее создать"
