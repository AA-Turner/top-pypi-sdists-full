class AssetType:

    def __init__(self, id=None, name=None, canProfile=None, canSample=None, *args, **kwargs):
        """
            Description:
                Asset type supported in torch. like table, views, database et cetera.
        :param id: Id of the asset type
        :param name: name of the type
        :param canProfile: true if we can profile that kind of assets else false
        :param canSample: true if we can sample the data else false
        """
        self.id = id
        self.name = name
        self.canSample = canSample
        self.canProfile = canProfile

    def __repr__(self):
        return f"AssetType({self.__dict__!r})"
