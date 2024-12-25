import os

user_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'name': {
        'type': 'string',
        'minlength': 1,
        'required': True,
    },
    'email': {
        'type': 'string',
        'minlength': 1,
        'required': True,
        'unique': True,
    },
    'role': {
        'type': 'string',
        'allowed': ["user", "manager", "admin"],
    },
}

DOMAIN = {'users': { 'schema': user_schema }}
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# if running from docker, use the docker container name, else use localhost
if 'DOCKER_CONTAINER' in os.environ:
    MONGO_HOST = 'mongodb'
else:
    MONGO_HOST = 'localhost'

URL_PREFIX = 'api'
