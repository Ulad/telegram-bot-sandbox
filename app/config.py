"""
Pedantic-settings always tries to determine the values of fields by reading them from environment variables.
By default, the name of the environment variable must match the name of the field.
The default values will still be used if the corresponding environment variable is not set.
Environment variables will always take precedence over the values loaded from the dotenv file.
Documentation: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from pprint import pformat

from app.utils.logger import logger


class Settings(BaseSettings):
    """Class for main settings"""
    model_config = SettingsConfigDict(env_file='.env', frozen=True)

    TOKEN: SecretStr


def get_cfg() -> Settings:
    """Initialize settings lazily"""
    cfg = Settings()
    logger.info(f'Project setting: \n{pformat(cfg.model_dump())}')
    return cfg
