import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG:      lambda record: f' {datetime.now().strftime("%d/%m %H:%M:%S")} \x1b[37mDEBUG\x1b[0m: {record.msg}',
        logging.INFO:       lambda record: f' {datetime.now().strftime("%d/%m %H:%M:%S")} \x1b[32mINFO\x1b[0m: \x1b[32m{record.msg}\x1b[0m',
        logging.WARNING:    lambda record: f' {datetime.now().strftime("%d/%m %H:%M:%S")} \x1b[33;20mWARNING\x1b[0m: {record.msg} ({record.filename}:{record.lineno})',
        logging.ERROR:      lambda record: f' {datetime.now().strftime("%d/%m %H:%M:%S")} \x1b[31;20mERROR\x1b[0m: {record.msg} ({record.filename}:{record.lineno})',
        logging.CRITICAL:   lambda record: f' {datetime.now().strftime("%d/%m %H:%M:%S")} \x1b[31;1mCRITICAL\x1b[0m: {record.msg} ({record.filename}:{record.lineno})'
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if log_fmt is None:
            log_fmt = self.format
        return log_fmt(record)


# create logger with 'spam_application'
logger = logging.getLogger("BOT")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)
