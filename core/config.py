from pathlib import Path
from typing import Type, Tuple

from anyio.functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, \
    YamlConfigSettingsSource


class Folder(BaseModel):
    name: str
    path: list[str] | Path


class AppConfig(BaseSettings):
    folders: list[Folder]
    backupFolder: Folder
    model_config = SettingsConfigDict(yaml_file='config.yaml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: YamlConfigSettingsSource,
        env_settings: YamlConfigSettingsSource,
        dotenv_settings: YamlConfigSettingsSource,
        file_secret_settings: YamlConfigSettingsSource,
    ) -> Tuple[YamlConfigSettingsSource, ...]:
        """
        Customize the order and type of configuration sources.
        """
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls), # Load from the yaml_file specified in model_config
            env_settings, # Environment variables will override YAML settings
            file_secret_settings,
        )



@lru_cache()
def get_settings() -> AppConfig:
    """Caches the settings object for performance."""
    return AppConfig()


