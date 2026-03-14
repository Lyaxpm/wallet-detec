from config import Settings, setup_logging
from interfaces.cli import run_cli


if __name__ == "__main__":
    settings = Settings()
    setup_logging(settings.log_level)
    run_cli()
