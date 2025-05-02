import logging
import sys

from etl.functions import FUNCTIONS
from etl.models import ETL
from etl.utils.utils import file_information, load_yaml

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)


def run(conf: ETL):
    """Runs the ETL pipeline

    param :conf, ETL: ETL object to run
    """
    for key in conf.order:
        for step in conf.pipeline.steps[key]:
            try:
                for sub_step in step:
                    logger.info("Running %s" % (sub_step))
                    process: dict = step[sub_step]
                    FUNCTIONS[process.get("function", None)](
                        **process, secrets=conf.secrets
                    )
                    if conf.meta_output and process.get("file_output", None):
                        file_information(process.get("file_output"), conf.meta_output)
            except KeyError as ex:
                logger.error("Got key error, skipping...")
                logger.error(ex)
                print(ex)


def main():
    """Main function"""
    args = sys.argv
    if len(args) < 2:
        raise ValueError("Missing pipeline yaml target...")
    conf = load_yaml(args[1])
    conf = ETL.from_dict(conf)
    if conf.secrets:
        conf.secrets = load_yaml(conf.secrets, dynamic=False)
    else:
        conf.secrets = load_yaml(args[2], dynamic=False)
    run(conf)


if __name__ == "__main__":
    """Entrypoint"""
    main()
