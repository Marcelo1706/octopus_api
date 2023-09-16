from os import environ

# Test Environment
IS_TEST = environ.get('IS_TEST', False)

# Database Credentials
MYSQL_ROOT_PASSWORD = environ.get('MYSQL_ROOT_PASSWORD')
MYSQL_DATABASE = environ.get('MYSQL_DATABASE')
MYSQL_USER = environ.get('MYSQL_USER')
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
MYSQL_HOST = environ.get('MYSQL_HOST', 'mariadb')
DATABASE_URL = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'  # noqa: E501

# Ministerio de Hacienda DTE Credentials
AUTH_URL = environ.get('AUTH_URL')
NIT = environ.get('NIT')
NRC = environ.get('NRC')
AUTH_PASSWORD = environ.get('AUTH_PASSWORD')
RECEPTION_URL = environ.get('RECEPTION_URL')

# SVFE Signature config
SIGNATURE_URL = environ.get('SIGNATURE_URL')
SIGNATURE_PASSWORD = environ.get('SIGNATURE_PASSWORD')
