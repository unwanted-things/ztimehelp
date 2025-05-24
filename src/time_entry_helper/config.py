"""Configuration management for Time Entry Helper."""

import os
from pathlib import Path
from typing import Dict, Optional


class Config:
    """Configuration manager for Time Entry Helper."""

    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / ".time_entry_helper"
        self.config_file = self.config_dir / "config.env"
        self._ensure_config_dir()
        self._config = self._load_config()

    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.touch()

    def _load_config(self) -> Dict[str, str]:
        """Load configuration from file."""
        config = {}
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a configuration value."""
        # First check environment variables
        env_value = os.environ.get(f"TIME_ENTRY_{key.upper()}")
        if env_value is not None:
            return env_value
        # Then check config file
        return self._config.get(key, default)

    def set(self, key: str, value: str):
        """Set a configuration value."""
        self._config[key] = value
        self._save_config()

    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, "w") as f:
            for key, value in self._config.items():
                f.write(f"{key}={value}\n")


# Global config instance
config = Config()
