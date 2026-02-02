import tgscheduler
import time


def task():
    print('Running task')


print('Init')
tgscheduler.start_scheduler()

print('Registering an interval task')
tgscheduler.add_interval_task(action=task, interval=5, initialdelay=5)

print('Sleeping')
while True:
    time.sleep(10)
