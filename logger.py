import logging
from colorlog import ColoredFormatter

LOG_LEVEL_SUCCESS = 123
LOG_LEVEL_HEADER = 222

def getLogger():
    """Return a logger with a default ColoredFormatter."""
    logging.addLevelName(LOG_LEVEL_SUCCESS, 'SUCCESS')
    logging.addLevelName(LOG_LEVEL_HEADER, 'HEADER')

    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'blue',
            'SUCCESS': 'green',
            'HEADER':'purple',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        },
        secondary_log_colors={
            'message': {
                'DEBUG': 'cyan',
                'INFO': 'blue',
                'SUCCESS': 'green',
                'HEADER': 'purple',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        },
        style='%'
    )


    logger = logging.getLogger('example')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    return logger