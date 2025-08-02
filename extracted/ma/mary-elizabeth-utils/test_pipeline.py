from pathlib import Path

import mary_elizabeth_utils as meu


def main():
    # Get the current directory
    current_dir = Path(__file__).parent.resolve()

    # Set up the logger
    logger = meu.setup_colored_logger(__name__)

    try:
        # Path to the config file
        config_path = current_dir / "test_config.yaml"

        # Create and run the data processor
        processor = meu.DataProcessor(str(config_path))
        processor.run()

        logger.info("Data processing pipeline completed successfully")
    except Exception as e:
        logger.error(f"Error in data processing pipeline: {e}")
        raise


if __name__ == "__main__":
    main()
