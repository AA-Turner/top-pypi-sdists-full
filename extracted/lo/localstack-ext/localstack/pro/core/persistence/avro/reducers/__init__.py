from localstack.utils.objects import singleton_factory


@singleton_factory
def register():
    # TODO: these reducers can be auto-discovered
    import localstack.pro.core.persistence.avro.reducers.threading  # noqa
