import logging
import pathlib

from yoyo import read_migrations, get_backend

from relocation_helper.appConfig import ApplicationConfiguration


class Migration:
    def __init__(self, config: ApplicationConfiguration):
        self.migrations = read_migrations(str(pathlib.Path(__file__).parent.absolute()) + '/migration')
        self.backend = get_backend("sqlite:///" + config.basePath)
        self.migLog = logging.getLogger("migration")

    def migrate(self):
        self.migLog.info("Start migration...")
        with self.backend.lock():
            # Apply any outstanding migrations
            self.backend.apply_migrations(self.backend.to_apply(self.migrations))
        self.migLog.info("Migration: success!")
