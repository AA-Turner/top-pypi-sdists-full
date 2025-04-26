
class ServiceLifecycle:
    def __init__(self):
        self.app_id = None
        self.active = False
        self.usable = True

    @classmethod
    def init(cls):
        """
        初始化服务
        该方法初始化系统服务，加载配置信息，并初始化所使用的资源。
        在实例化后调用，或在修改配置信息后再次调用
        """
        raise NotImplementedError("init() must be implemented by subclasses")

    @classmethod
    def startup(cls):
        """
        启动服务
        该方法启动系统服务，只设置状态为可使用。
        只有状态可已启动，才可以对外提供服务。
        在初始化后调用或停止后再次调用；当修改配置文件的内容后，需要重新初始化并启动。
        """
        cls.active = True

    @classmethod
    def shutdown(cls):
        """
        停止服务
        该方法停止系统服务，只设置状态为不可使用，并不释放资源。
        当状态为未启动，不可以对外提供服务。
        在停止后，可以重新启动。
        """
        cls.active = False

    @classmethod
    def reset(cls):
        """
        复位服务
        该方法停止系统服务后，再重新启动。
        重启前，需停机并清理资源，然后才可重启动。
        """
        cls.shutdown()
        cls.destroy()
        cls.init()
        cls.startup()

    @classmethod
    def destroy(cls):
        """
        中止服务
        """
        raise NotImplementedError("destroy() must be implemented by subclasses")

    @property
    def info(self):
        """
        获取服务管理器信息
        """
        name = self.__class__.__name__

        schema = getattr(self.__class__, '__doc__', None)
        if schema:
            name = schema.split("\n")[0].strip()

        return {
            'id': self.__class__.__name__,
            'name': name,
            'app_id': self.app_id,
            'active': self.active,
            'usable': self.usable
        }