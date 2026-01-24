import click
import logging
import sys
from anc.version import __version__

from anc.cli import deployment
from anc.cli import dataset
from anc.cli import quantization
from anc.cli import evaluation

from anc.cli.load_testing import loadtest
from anc.cli.util import click_group

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("anc")


@click.version_option(__version__, "-v", "--version")
@click.option('--log-level', 
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                               case_sensitive=False),
              default='INFO',
              help='Set the logging level')
@click_group(context_settings=CONTEXT_SETTINGS)
def main(log_level):
    # Configure logging with specified level
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    pass


#deployment.add_command(main)
dataset.add_command(main)
quantization.add_command(main)
evaluation.add_command(main)
main.add_command(loadtest)

if __name__ == "__main__":
    main()
