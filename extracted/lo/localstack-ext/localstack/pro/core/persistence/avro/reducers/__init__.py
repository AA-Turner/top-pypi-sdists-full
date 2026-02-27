from localstack.utils.objects import singleton_factory


@singleton_factory
def register():
    # TODO: these reducers can be auto-discovered
    import localstack.pro.core.persistence.avro.reducers.threading  # noqa
    import localstack.pro.core.persistence.avro.reducers.cryptography  # noqa
    import localstack.pro.core.persistence.avro.reducers.sqs  # noqa
    import localstack.pro.core.persistence.avro.reducers.cognito  # noqa
