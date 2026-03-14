from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    hermes_base_url: str = os.getenv("HERMES_BASE_URL", "https://hermes-agent.nousresearch.com/v1")
    hermes_api_key: str = os.getenv("HERMES_API_KEY", "")
    hermes_model: str = os.getenv("HERMES_MODEL", "Hermes-3-Llama-3.1-70B")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
