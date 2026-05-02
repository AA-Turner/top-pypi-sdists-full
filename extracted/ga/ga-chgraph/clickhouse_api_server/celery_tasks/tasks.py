import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery_tasks.celery_app import app
from celery_tasks.plato_client import PlatoClient


@app.task
def graph_calculation_task(sub_graph, task_id, calculation_type):
    plato_client = PlatoClient(sub_graph, task_id, calculation_type)
    plato_client.run()


if __name__ == "__main__":
    graph_calculation_task.delay("7cf53539_81d6_4986_9745_86d2acfc97c6", 8, 'pagerank')



