import os
from dotenv import load_dotenv


# region Logging
import logging

console = logging.getLogger(__name__)

class CustomFormatter(logging.Formatter):
    red = "\033[31;20m"
    yellow = "\033[33;20m"
    purple = "\033[35;20m"
    grey = "\033[38;20m"

    bold_black = "\033[30;1m"
    bold_red = "\033[31;1m"
    bold_green = "\033[32;1m"
    bold_yellow = "\033[33;1m"
    bold_blue = "\033[34;1m"
    bold_purple = "\033[35;1m"
    bold_grey = "\033[38;1m"

    reset = "\033[0m"

    time = f"{bold_black}%(asctime)s{reset}"
    message = f"{purple}%(name)s{reset} %(message)s"
    log_level = " %(levelname)-8s "

    FORMATS = {
        logging.DEBUG: time + bold_green + log_level + reset + message,
        logging.INFO: time + bold_blue + log_level + reset + message,
        logging.WARNING: time + bold_yellow + log_level + reset + message,
        logging.ERROR: time + bold_red + log_level + reset + message,
        logging.CRITICAL: time + bold_red + log_level + reset + message,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
console.setLevel(logging.DEBUG)
console.addHandler(console_handler)
# endregion

# region Environment
load_dotenv(".env")

def get_token() -> str:
    TOKEN = os.getenv("TOKEN")
    if TOKEN is None:
        console.error("Token not found")
        raise Exception("Token not found")
    return TOKEN


def get_token_alt() -> str:
    TOKEN_ALT = os.getenv("TOKEN_ALT")
    if TOKEN_ALT is None:
        console.error("Token not found")
        raise Exception("Token not found")
    return TOKEN_ALT
# endregion

DEFAULT_CSV_PATH = os.path.abspath("data/data.csv")
DEFAULT_DB_PATH = os.path.abspath("data/data.db")


if __name__ == "__main__":
    console.info("Info log")
    console.debug("Debug log")
    console.warning("Warning log")
    console.error("Error log")
    console.critical("Critical log")

    console.info(f"TOKEN: {get_token():>4}")
    console.info(f"DATA_CSV: {DEFAULT_CSV_PATH}")
