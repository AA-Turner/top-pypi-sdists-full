from pathlib import Path

import mary_elizabeth_utils as meu


def main() -> None:
    logger = meu.setup_colored_logger(__name__)

    try:
        config_path = Path(__file__).parent / "config.yaml"
        processor = meu.DataProcessor(str(config_path))
        processor.run()
        logger.info("Data processing pipeline completed successfully")
    except Exception as e:
        logger.error(f"Error in data processing pipeline: {e!s}")
        raise


if __name__ == "__main__":
    main()
