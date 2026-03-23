from dependency_injector import containers, providers

from .service import Service, ServiceWithCallable


class SubContainer(containers.DeclarativeContainer):

    int_object = providers.Object(1)


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    service = providers.Factory(Service)

    service_with_callable = providers.Factory(ServiceWithCallable)

    sub = providers.Container(SubContainer)
