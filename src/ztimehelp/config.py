import os
from pathlib import Path
from typing import Dict, Optional


class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".ztimehelp"
        self.config_file = self.config_dir / "config.env"
        self._ensure_config_dir()
        self._config = self._load_config()

    def _ensure_config_dir(self):
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.touch()

    def _load_config(self) -> Dict[str, str]:
        config = {}
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip().replace('"','').replace("'",'')
        return config

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._config.get(key, default)


config = Config()
