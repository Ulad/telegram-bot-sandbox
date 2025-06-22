from logging import getLogger, Formatter, LogRecord
from logging.config import dictConfig
from typing import ClassVar


class CustomColoredFormatter(Formatter):
    """Colored output formatter."""
    COLORS: ClassVar = {
        'DEBUG': "\033[0;37m",   # Light gray
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\x1b[31;1m',  # Bold red
        'RESET': '\033[0m'       # Reset color
    }

    def format(self, record: LogRecord) -> str:
        """Format the given log record into a colored string."""
        formatted_message = super().format(record)
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        return f"{level_color}{formatted_message}{self.COLORS['RESET']}"


dictConfig({
    'version': 1,
    'formatters': {
        'detailedFormatter': {
            'format': '%(asctime)s - [%(levelname)-8s] - %(module)s - %(lineno)s - %(funcName)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%z'
        },
        'coloredFormatter': {
            '()': CustomColoredFormatter,
            'format': '%(asctime)s - [%(levelname)-8s] - %(message)s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'coloredFormatter',
            'stream': 'ext://sys.stdout'
        },
        'fileHandler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailedFormatter',
            'filename': 'logs.log',
            'mode': 'a',
            'maxBytes': 10*1024*1024, # 10 MB
            'backupCount': 5, # Keep up to 5 backup files
            'encoding': 'utf8'
        }
    },
    'root': {'level': 'DEBUG', 'handlers': ['consoleHandler', 'fileHandler']}
})

logger = getLogger(__name__)
