import logging
from dataclasses import dataclass
from typing import Optional

from relocation_helper import nlu
from relocation_helper.appConfig import ApplicationConfiguration
from relocation_helper.dao import Dao

log = logging.getLogger("skill_logic")


@dataclass
class YaDRequestSessionObject:
    message_id: int
    session_id: str
    new: bool


@dataclass
class YaDRequestObjectNlu:
    tokens: list


@dataclass
class YaDRequestObject:
    command: str
    original_utterance: str
    nlu: YaDRequestObjectNlu


@dataclass
class YaDRequest:
    request: YaDRequestObject
    version: str
    session: YaDRequestSessionObject


@dataclass
class YaDResponseObject:
    text: str
    end_session: bool
    tts: Optional[str] = None


@dataclass
class YaDResponse:
    response: YaDResponseObject
    version: str = "1.0"


class SkillLogic:
    def __init__(self, appConfig: ApplicationConfiguration, daoObject: Dao):
        self.config = appConfig
        self.dao = daoObject

    def process(self, req: YaDRequest):
        log.debug("Command: %s", req.request.command)
        endSession = req.session.new and \
                     nlu.atLeastOneWordFromEachGroupIn(req.request.command,
                                                       [["создавать", "добавлять", "сделать", "положить"]])
        resp = None
        if (not req.request.command and not req.request.original_utterance) or "помоги" == req.request.command:
            resp = YaDResponse(
                YaDResponseObject(
                    text="Скажи что делать:к примеру, создай новую коробку Игрушки, или добавь в коробку Игрушки предмет Сортер",
                    end_session=endSession
                )
            )
        elif nlu.atLeastOneWordFromEachGroupIn(req.request.command, [["создавать", "сделать"], "коробка"]):
            boxName = req.request.command.split(" коробку ")[1].strip()
            if self.dao.isBoxExists(boxName):
                resp = YaDResponse(
                    YaDResponseObject(
                        text="Коробка %s уже есть, не нужно снова её создавать, можете помещать в неё вещи" % boxName,
                        end_session=endSession
                    )
                )
            else:
                self.dao.addBox(boxName)
                resp = YaDResponse(
                    YaDResponseObject(
                        text="Коробка %s создана, теперь можно помещать в нее вещи" % boxName,
                        end_session=endSession
                    )
                )
        elif nlu.atLeastOneWordFromEachGroupIn(req.request.command, [["добавлять", "полагать", "покладь"], "коробка", "предмет"]):
            boxName = req.request.command.split(" коробку ")[1].split(" предмет ")[0].strip()
            item = req.request.command.split(" предмет ")[1].strip()
            boxId = self.dao.getBoxId(boxName)
            if boxId:
                self.dao.addItemIntoBox(boxId, item)
                resp = YaDResponse(
                    YaDResponseObject(
                        text="Запомнила: %s в коробке %s." % (item, boxName),
                        end_session=endSession
                    )
                )
            else:
                resp = YaDResponse(
                    YaDResponseObject(
                        text="Не могу найти коробку с названием: %s, нужно сперва ее создать" % boxName,
                        end_session=endSession
                    )
                )
        if resp is None:
            resp = YaDResponse(
                YaDResponseObject(
                    text="Не понимаю, что нужно делать, если нужно помочь с командами, скажи: помоги",
                    end_session=endSession
                )
            )
        if endSession:
            resp.response.text += ". До скорых встреч!"
        return resp
