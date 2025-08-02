from python_sdk_remote.our_object import OurObject


class HelperMysqlObject(OurObject):
    # use this as test class, naming it TestMysqlObject results in a Warning:
    # cannot collect test class 'TestMysqlObject' because it has a __init__ constructor (from: database_mysql_local/src/test_mysql_object.py)
    def __init__(self, **kwargs):
        test_mysql_fields = {
            "test_mysql_id",
            "number",
            "identifier",
            "name",
            "group",
            "unique_int_column",
            "point",
            "polygon",
            "visibility_id",
            "is_test_data",
            "start_timestamp",
            "end_timestamp",
            "created_timestamp",
            "created_user_id",
            "created_real_user_id",
            "created_effective_user_id",
            "created_effective_profile_id",
            "updated_timestamp",
            "updated_user_id",
            "updated_real_user_id",
            "updated_effective_user_id",
            "updated_effective_profile_id",
        }

        for field, value in kwargs.items():
            if field in test_mysql_fields:
                setattr(self, field, value)

    def get_name(self):
        return self.name

    def __str__(self):
        return "test_mysql: " + str(self.__dict__)

    def __repr__(self):
        return "test_mysql: " + str(self.__dict__)

    def to_dict(self):
        return self.__dict__
