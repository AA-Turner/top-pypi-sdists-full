from abstract_utilities import get_env_value
ENV_PATH = '/home/solcatcher/.env'
CRED_VALUES = {
    "postgres":{
        "prefix":'SOLCATCHER_POSTGRESQL',"defaults":{
        "host":'localhost',
        "port":'1234',
        "user":'solcatcher',
        "name":'solcatcher',
        "password":'solcatcher'
    }
        },
    "amqp":{
        "prefix":'SOLCATCHER_AMQP',
        "defaults":{
            "host":'localhost',
            "port":'1234',
            "user":'solcatcher',
            "name":'solcatcher',
            "password":'solcatcher'
            }
        }
    }
SOLCATCHER_POSTGRESQL_DBURL = get_env_value("SOLCATCHER_POSTGRESQL_DBURL")
