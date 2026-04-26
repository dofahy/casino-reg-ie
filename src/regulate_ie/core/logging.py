import logging
import sys


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)],
    )


"""
import platform
import time

from pythonjsonlogger.json import JsonFormatter as BaseFormatter

HOSTNAME = platform.node()

class JsonFormatter(BaseFormatter):
    converter = time.gmtime

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record["hostname"] = HOSTNAME

        exc = getattr(record, "exc_info", None)
        if exc and len(exc) > 1:
            exc_value = exc[1]

            query = getattr(exc_value, "_exc_query", None)
            if query:
                log_record["query"] = query

        # log_record["version"] = VERSION

def setup_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    formatter = JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)
    root.addHandler(handler)

    return root
 """
