import atexit
import json
import logging.config
import logging.handlers
import pathlib

# we can use yaml too but there is no yaml parser built in in python but for json yes

logger = logging.getLogger(__name__)  # __name__ is a common choice


def setup_logging():
    config_file = pathlib.Path("./app/logs/log_config/config_filter_stdout_stderr.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main():
    setup_logging()
    logging.basicConfig(level="INFO")
    logger.debug("debug message", extra={"x": "hello"}) # "extra" we can use it to add more information to our json logs
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()