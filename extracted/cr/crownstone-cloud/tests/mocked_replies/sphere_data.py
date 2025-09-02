sphere_data = [
    {
        "name": "my_awesome_sphere",
        "uid": 69,
        "uuid": "uuid",
        "meshAccessAddress": "mesh_access_address",
        "aiName": "smart_ai",
        "aiSex": "null",
        "exitDelay": 600,
        "gpsLocation": {
            "lat": 69,
            "lng": 69
        },
        "id": "my_awesome_sphere_id",
        "ownerId": "owner_id",
        "createdAt": "date_created",
        "updatedAt": "date_updated"
    },
    {
        "name": "my_awesome_sphere_2",
        "uid": 42,
        "uuid": "uuid",
        "meshAccessAddress": "mesh_access_address",
        "aiName": "super_smart_ai",
        "aiSex": "null",
        "exitDelay": 600,
        "gpsLocation": {
            "lat": 42,
            "lng": 42
        },
        "id": "my_awesome_sphere_id_2",
        "ownerId": "owner_id",
        "createdAt": "date_created",
        "updatedAt": "date_updated"
    }
]

key_data = [
  {
    "sphereId": "my_awesome_sphere_id_2",
    "sphereKeys": [
      {
        "id": "admin_id",
        "keyType": "ADMIN_KEY",
        "key": "admin_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "member_id",
        "keyType": "MEMBER_KEY",
        "key": "member_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "basic_id",
        "keyType": "BASIC_KEY",
        "key": "basic_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "localization_id",
        "keyType": "LOCALIZATION_KEY",
        "key": "localization_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "service_data_id",
        "keyType": "SERVICE_DATA_KEY",
        "key": "service_data_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "mesh_application_id",
        "keyType": "MESH_APPLICATION_KEY",
        "key": "mesh_application_key",
        "ttl": 0,
        "createdAt": "date_created"
      },
      {
        "id": "mesh_network_id",
        "keyType": "MESH_NETWORK_KEY",
        "key": "mesh_network_key",
        "ttl": 0,
        "createdAt": "date_created"
      }
    ]
  }
]

expected_key_data = {
    'ADMIN_KEY': 'admin_key',
    'MEMBER_KEY': 'member_key',
    'BASIC_KEY': 'basic_key',
    'LOCALIZATION_KEY': 'localization_key',
    'SERVICE_DATA_KEY': 'service_data_key',
    'MESH_APPLICATION_KEY': 'mesh_application_key',
    'MESH_NETWORK_KEY': 'mesh_network_key'
}
