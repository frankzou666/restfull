import logging


# SECRET_KEY do not modify
SECRET_KEY = '5a21e5d9bbde4f379378f48a6727545d'

# jwt session token expire time (seconds)
JWTSESSIONTIME = 36000

LOGLEVEL = logging.INFO

LISTENHOST = '0.0.0.0'
LISTENPORT = '5000'

# True of False
PROD = False

# mysql database configure
MYSQLHOST = '192.168.30.66'
MYSQLPORT = '22330'
MYSQLUSER = 'app'
MYSQLPWD = 'app123456'
MYSQLDBNAME = 'app'
