from .console import ProcessCommunicationEventHandler


def main():
    handler = ProcessCommunicationEventHandler()
    handler.run_forever()


if __name__ == '__main__':
    main()