import lazy_loader

__getattr__, __dir__, _ = lazy_loader.attach_stub(__name__, __file__)
