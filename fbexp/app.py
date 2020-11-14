'''Application main function'''

import logging
import logging.config
import os
import time

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from .fb_exporter import FritzBoxExporter
from .metrics_config import METRICS_CFG2

from . import logger


DEFAULT_HOST = 'fritz.box'
DEFAULT_PORT = '8765'
DEFAULT_LOGLEVEL = 'info'


def setup_logging(level):
    '''Set up the logging output.'''

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s')

    logging.config.dictConfig({
        'version': 1,
        'loggers': {
            'fbexp': {
                'level': level
            }
        }
    })


def main():
    '''Main method initializing the application and starting the exporter.'''

    level = os.getenv('LOGLEVEL', DEFAULT_LOGLEVEL).upper()

    setup_logging(level)

    user = os.getenv('FRITZ_USER', None)
    password = os.getenv('FRITZ_PASS', None)

    if (user is None) or (password is None):
        logger.error(
            'User and/or password to log in to FritzBox are not available. '
            'Please make sure to set FRITZ_USER and FRITZ_PASS environment '
            'variables correctly.')

        return 1

    host = os.getenv('FRITZ_HOST', DEFAULT_HOST)

    fb_exporter = FritzBoxExporter(
        host,
        user,
        password,
        METRICS_CFG2)

    REGISTRY.register(fb_exporter)

    # Start up the server to expose the metrics.
    port = int(os.getenv('FRITZ_EXPORTER_PORT', DEFAULT_PORT))
    logger.info(f'Starting web server on port {port}.')

    start_http_server(port)

    while True:
        time.sleep(10000)
