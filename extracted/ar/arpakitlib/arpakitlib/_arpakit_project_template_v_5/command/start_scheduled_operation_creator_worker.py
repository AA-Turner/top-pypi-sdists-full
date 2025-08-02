from project.core.util import setup_logging
from project.operation_execution.scheduled_operation_creator_worker import create_scheduled_operation_creator_worker


def __command():
    setup_logging()
    worker = create_scheduled_operation_creator_worker()
    worker.sync_safe_run()


if __name__ == '__main__':
    __command()
