# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class DescribeDatabaseResponseBody(DaraModel):
    def __init__(
        self,
        access_privilege: str = None,
        character_set_name: str = None,
        collate: str = None,
        conn_limit: str = None,
        ctype: str = None,
        dbinstance_id: str = None,
        database_name: str = None,
        description: str = None,
        owner: str = None,
        request_id: str = None,
        size: str = None,
        table_space: str = None,
    ):
        # The access control information.
        self.access_privilege = access_privilege
        # The character set.
        # 
        # For the valid values, refer to the References at https://www.postgresql.org/docs/current/multibyte.html.
        self.character_set_name = character_set_name
        # The locale setting of the database, which specifies the string comparison and sorting rules.
        # >
        # > - The locale must be compatible with the character set specified by the CharacterSetName parameter.
        # > - Valid values: You can run the SELECT DISTINCT collname FROM pg_collation; command to query the valid values. If this parameter is not specified, the default value is en_US.utf8.
        self.collate = collate
        # The maximum number of concurrent connections. A value of -1 indicates no limit.
        self.conn_limit = conn_limit
        # The locale setting of the database, which specifies the character classification and case conversion rules.
        # > 
        # > - The locale must be compatible with the character set specified by the CharacterSetName parameter.
        # > - You can run the SELECT DISTINCT collctype FROM pg_collation; command to query the valid values. If this parameter is not specified, the default value is en_US.utf8.
        self.ctype = ctype
        # The instance ID.
        self.dbinstance_id = dbinstance_id
        # The name of the database.
        # 
        # - It can contain only letters, digits, and underscores (_).
        # 
        # - It must start with a letter.
        # 
        # - It cannot exceed 63 characters in length.
        self.database_name = database_name
        # The description of the database.
        self.description = description
        # The owner of the database.
        # 
        # - It can contain only lowercase letters, digits, and underscores (_).
        # 
        # - It must start with a lowercase letter and end with a lowercase letter or a digit.
        # 
        # - It cannot start with gp.
        # 
        # - It must be 2 to 16 characters in length.
        self.owner = owner
        # The request ID.
        self.request_id = request_id
        # The size of the database.
        self.size = size
        # The tablespace of the database.
        self.table_space = table_space

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.access_privilege is not None:
            result['AccessPrivilege'] = self.access_privilege

        if self.character_set_name is not None:
            result['CharacterSetName'] = self.character_set_name

        if self.collate is not None:
            result['Collate'] = self.collate

        if self.conn_limit is not None:
            result['ConnLimit'] = self.conn_limit

        if self.ctype is not None:
            result['Ctype'] = self.ctype

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.database_name is not None:
            result['DatabaseName'] = self.database_name

        if self.description is not None:
            result['Description'] = self.description

        if self.owner is not None:
            result['Owner'] = self.owner

        if self.request_id is not None:
            result['RequestId'] = self.request_id

        if self.size is not None:
            result['Size'] = self.size

        if self.table_space is not None:
            result['TableSpace'] = self.table_space

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccessPrivilege') is not None:
            self.access_privilege = m.get('AccessPrivilege')

        if m.get('CharacterSetName') is not None:
            self.character_set_name = m.get('CharacterSetName')

        if m.get('Collate') is not None:
            self.collate = m.get('Collate')

        if m.get('ConnLimit') is not None:
            self.conn_limit = m.get('ConnLimit')

        if m.get('Ctype') is not None:
            self.ctype = m.get('Ctype')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('DatabaseName') is not None:
            self.database_name = m.get('DatabaseName')

        if m.get('Description') is not None:
            self.description = m.get('Description')

        if m.get('Owner') is not None:
            self.owner = m.get('Owner')

        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')

        if m.get('Size') is not None:
            self.size = m.get('Size')

        if m.get('TableSpace') is not None:
            self.table_space = m.get('TableSpace')

        return self

