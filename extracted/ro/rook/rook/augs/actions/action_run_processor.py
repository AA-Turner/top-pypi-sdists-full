class ActionRunProcessor(object):
    NAME = 'script'

    def __init__(self, configuration, processor_factory):
        self.processor = processor_factory.get_processor(configuration['operations'])

    def execute(self, aug_id, report_id, namespace, output):
        self.processor.process(namespace)
        output.send_user_message(aug_id, report_id, namespace['store'])
