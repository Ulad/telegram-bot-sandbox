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
from os import getenv

from bot.utils.logger import log


class Settings(BaseSettings):
    """Class for main settings"""

    TOKEN: SecretStr


class DevSettings(Settings):
    """Class for development settings"""

    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8")
    ENV: str = "dev"


class ProdSettings(Settings):
    """Class for production settings"""

    model_config = SettingsConfigDict(env_file=".env.prod", env_file_encoding="utf-8")
    ENV: str = "prod"


def get_cfg() -> Settings:
    """Return the settings object based on the environment."""

    env = getenv("ENV", "dev")

    if env.lower() in ("dev", "development"):
        return DevSettings()
    if env.lower() in ("prod", "production"):
        return ProdSettings()

    raise ValueError("Invalid environment. Must be 'dev' or 'prod'.")


cfg = get_cfg()
log.info(f"Project setting: {pformat(cfg.model_dump())}")
