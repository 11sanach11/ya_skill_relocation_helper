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
from relocation_helper.appConfig import prepareConfig

config = prepareConfig()
if config.server.engine == "gevent":
    from gevent import monkey

    monkey.patch_all()

import logging
from logging.handlers import RotatingFileHandler
import systemd.daemon

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s',
                    handlers=filter(
                        lambda handler: handler is not None,
                        [logging.StreamHandler() if not config.logOnlyInFile else None,
                         RotatingFileHandler(
                             backupCount=100,
                             maxBytes=1024 * 1024 * 10,
                             filename=config.logFileName)]))
from time import sleep
from relocation_helper.relocationHelper import RelocationHelper

log = logging.getLogger()

if __name__ == '__main__':
    log.info('Starting up ...')
    print("Start helper...")
    RelocationHelper(config)
    log.info('Startup complete')
    systemd.daemon.notify(systemd.daemon.Notification.READY)
    print("Helper started.")
    while True:
        sleep(100)
