#Source https://github.com/torfsen/python-systemd-tutorial

import logging
import time
import argparse

from systemd import daemon
from config_loader.config import BaseConfig
from utils import journald_handler, logLevel

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        nargs='*',
        type=str,
        default='/etc/butcher/butcher.ini',
        help='The telemetry you want to get: orders, hides, oee. Blank means all')
    config_file = parser.parse_args().config
    logger.addHandler(journald_handler)
    logger.setLevel(logLevel)

    logger.info("Starting up ...")
    config = BaseConfig(path=config_file)
    logger.info("Startup complete, config is loaded")

    # Tell systemd that our service is ready
    logger.info("Services is ready)")
    daemon.notify(daemon.Notification.READY)
    logger.info("Configuration recap:")
    logger.info(f"Main Loop sleep timer: {config.sleep}")
    logger.info(f"Warning level: {config.warning_lvl}")
    parser = config.parser

    while True:
        parser.start()
        time.sleep(config.sleep)
        parser.notify(config=config)
