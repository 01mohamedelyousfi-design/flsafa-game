from loguru import logger


def configure() -> None:
    logger.info("Opik tracing is disabled.")
    return


def get_dataset(name: str):
    return None


def create_dataset(name: str, description: str, items: list[dict]):
    return None
