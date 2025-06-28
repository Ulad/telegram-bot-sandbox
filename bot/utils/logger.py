from logging import getLogger, Formatter, LogRecord
from logging.config import dictConfig
from typing import ClassVar
from re import sub, Match


def decode_unicode_escapes(text: str) -> str:
    r"""
    Decode Unicode escape sequences in the format `\\uXXXX` within a string.

    Replaces all occurrences of escape sequences like `\\u03A9` (which represent 'Ω')
    with their corresponding Unicode characters. The input escape sequences must use
    exactly 4 hexadecimal digits and follow the format `\\uXXXX`.

    >>> decode_unicode_escapes("Greek omega: \\\\u03A9")
    'Greek omega: Ω'
    """

    def decode_match(match: Match[str]) -> str:
        """Convert regex match to Unicode character"""
        return chr(int(match.group(1), 16))

    return sub(r"\\\\u([0-9a-fA-F]{4})", decode_match, text)


class BaseFormatter(Formatter):
    """
    Base output formatter with conditional encoding. The formatted message
    is converted to a string representation of its UTF-8 encoded bytes.
    Other messages are returned as normal strings.
    """

    def format(self, record: LogRecord) -> str:
        r"""
        Format the given log record and returns the string representation of the UTF-8 encoded bytes.

        >>> from logging import makeLogRecord
        >>> formatter = BaseFormatter(fmt='%(message)s')
        >>> formatter.format(makeLogRecord({'msg': 'The server returned: \\\\u03A9'}))
        'The server returned: Ω'

        >>> formatter.format(makeLogRecord({'msg': 'Server status: 200 OK'}))
        'Server status: 200 OK'
        """
        msg = super().format(record)
        return decode_unicode_escapes(msg) if "The server returned:" in record.message else msg


class ColoredFormatter(BaseFormatter):
    """Colored output formatter."""

    COLORS: ClassVar = {
        "DEBUG": "\033[0;37m",  # Light gray
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\x1b[31;1m",  # Bold red
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record: LogRecord) -> str:
        """Format the given log record into a colored string."""
        msg = super().format(record)
        level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{level_color}{msg}{self.COLORS['RESET']}"


dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "coloredFormatter": {
                "()": ColoredFormatter,
                "format": "%(asctime)s - [%(levelname)-8s] - %(module)s - %(lineno)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "fileFormatter": {
                "()": BaseFormatter,
                "format": "%(asctime)s - [%(levelname)-8s] - %(module)s - %(lineno)s - %(name)s - %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "coloredFormatter",
                "stream": "ext://sys.stdout",
            },
            "fileHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "fileFormatter",
                "filename": "logs.log",
                "mode": "a",
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,  # Keep up to 5 backup files
                "encoding": "utf8",
            },
        },
        "loggers": {
            "TeleBot": {
                "level": "DEBUG",
                "propagate": True,
            },
            "urllib3": {
                "level": "DEBUG",
                "propagate": False,
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
        },
    }
)

log = getLogger(__name__)
