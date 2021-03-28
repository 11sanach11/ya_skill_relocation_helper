# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import json
import logging
import pathlib
import threading
from dataclasses import asdict
from functools import wraps

from bottle import TEMPLATE_PATH, HTTPResponse, request, response, get, post, run as run_bottle
from dacite import from_dict

TEMPLATE_PATH.append(str(pathlib.Path(__file__).parent.absolute()) + '/templates/')

from relocation_helper.appConfig import ApplicationConfiguration
from relocation_helper.dao import Dao
from relocation_helper import __version__
from relocation_helper.skillLogic import SkillLogic
from relocation_helper.skillLogic import YaDRequest

log = logging.getLogger("bottleServer")

dao: Dao = None
skillLogic: SkillLogic = None


@post('/relocationHelper')
def relocationHelper():
    raw_body = json.load(request.body)
    log.info("Raw body: %s", raw_body)
    req = from_dict(YaDRequest, raw_body)
    resp = skillLogic.process(req)
    raw_response = asdict(resp)
    log.info("Response: %s", raw_response)
    return raw_response


def _getTemplateFile(templateName):
    return str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + templateName


@get("/info")
def info():
    return {"version": __version__, "app": "telegram_mailing_helper"}


class BottleServer(threading.Thread):

    def __init__(self, config: ApplicationConfiguration, daoObject: Dao):
        global dao, skillLogic
        threading.Thread.__init__(self, name=__name__)
        dao = daoObject
        skillLogic = SkillLogic(config, daoObject)
        self.daemon = True
        self.config = config

    def logToLogger(self, fn):
        @wraps(fn)
        def _logToLogger(*args, **kwargs):
            try:
                actual_response = fn(*args, **kwargs)
                log.info('%s: %s %s %s %s',
                         request.get_header("Ssl-Dn", "non-ssl"),
                         request.remote_addr,
                         request.method,
                         request.url,
                         response.status)
                return actual_response
            except Exception as e:
                if type(e) is HTTPResponse and e.status_code in [302, 303]:
                    log.info("redirect %s %s %s %s",
                             request.remote_addr,
                             request.method,
                             request.url,
                             response.status)
                else:
                    log.exception("Exception while call %s %s %s %s:",
                                  request.remote_addr,
                                  request.method,
                                  request.url,
                                  response.status)
                raise e

        return _logToLogger

    def run(self) -> None:
        run_bottle(host=self.config.server.host,
                   port=self.config.server.port,
                   server=self.config.server.engine,
                   plugins=[self.logToLogger],
                   quiet=True)
