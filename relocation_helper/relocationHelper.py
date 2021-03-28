#!/usr/bin/env python3
import sys
from signal import SIGINT, SIGTERM, SIGABRT, signal
from time import sleep

import systemd

from relocation_helper.appConfig import ApplicationConfiguration

use_gevent = False
if use_gevent:
    from gevent import monkey

    monkey.patch_all()
import logging

from relocation_helper.migration import Migration
from relocation_helper.dao import Dao
from relocation_helper.server import BottleServer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)


class RelocationHelper:

    def signal_handler(self, signum, frame) -> None:
        print("Try to stop helper...")
        while True:
            try:
                break
            except Exception:
                log.exception("Exception while stop telegram bot")
            log.info("Sleep 1 second...")
            sleep(1)
        log.info("Application stopped")
        systemd.daemon.notify(systemd.daemon.Notification.STOPPING)
        print("Helper had been stopped")
        sys.exit()

    def __init__(self, appConfig: ApplicationConfiguration):
        log.info("Start the application")
        self.migration = Migration(config=appConfig)
        self.migration.migrate()

        self.dao = Dao(appConfig)
        self.server = BottleServer(appConfig, self.dao)
        self.server.start()

        for sig in (SIGINT, SIGTERM, SIGABRT):
            signal(sig, self.signal_handler)
