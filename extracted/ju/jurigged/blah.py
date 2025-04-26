# import sys
# import time
# import logging
# from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler, FileSystemEventHandler


# class JuriggedHandler(FileSystemEventHandler):
#     def on_modified(self, event):
#         print(event.src_path)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     path = sys.argv[1] if len(sys.argv) > 1 else '.'
#     # help(FileSystemEventHandler)
#     event_handler = JuriggedHandler()
#     observer = Observer()
#     # observer.schedule(event_handler, path, recursive=True)
#     observer.schedule(event_handler, "blah.py", recursive=False)
#     observer.start()
#     try:
#         while True:
#             time.sleep(0.1)
#     finally:
#         observer.stop()
#         observer.join()


import os

from jurigged import live


def filt(path):
    return path.endswith(".py") and path.startswith(os.getcwd())


thing = [1, 2, 3]


def foo(x):
    return x * thing


def flab():
    return 13 / 0


class Bob:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def lol(self):
        return 4


b = Bob(7, 8)


def deco(fn):
    def decorayted(*args, **kwargs):
        return fn(*args) + 1

    return decorayted


@deco
def woofers(x):
    return x * x


if __name__ == "__main__":
    collector = live.Collector(filt)
    collector.start()
    # collector.stop()
    # xx = importlib.util.find_spec("ovld")
    # print(xx)

    try:
        # while True:
        #     time.sleep(0.1)
        import code

        code.interact(local=locals())
    finally:
        collector.stop()
        collector.join()
