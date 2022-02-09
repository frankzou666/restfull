

from flask import Flask
from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from restfull.views.views import view
from restfull.views.api import apiview
from restfull.views.author import apiauthor
from restfull.views.book import apibook
from restfull.views.user import apiuser
import os
import pymysql
import flask_monitoringdashboard as monitoringdashboard
from flask_jwt_extended import JWTManager
from datetime import timedelta


# new app
app = Flask(__name__)
app.config.from_object('config')
app.config['APPDIR'] = os.getcwd()
app.config['SECRET_KEY'] = 'the random string'


# monitoringdashboard
#monitoringdashboard.config.blueprint_name = '/monitor/dashboard'
monitoringdashboard.bind(app=app)

#jwt
jwt = JWTManager(app)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=app.config['JWTSESSIONTIME'])

# config logger
if app.config['PROD']:
    logging.basicConfig(level=app.config['LOGLEVEL'],
                        format='%(levelname)s:%(asctime)s-%(filename)s-%(module)s-%(lineno)d:%(message)s',
                        filename=os.path.join(app.config['APPDIR'],'myapp','logs','app.log'))
else:
    logging.basicConfig(level=app.config['LOGLEVEL'],
                        format='%(levelname)s:%(asctime)s-%(filename)s-%(module)s-%(lineno)d:%(message)s'
                        )
# create dbengine

engine = create_engine( "mysql+pymysql://"+app.config['MYSQLUSER']+":" \
                       +app.config['MYSQLPWD']+"@"
                       +app.config['MYSQLHOST']+":" \
                       +str(app.config['MYSQLPORT']) \
                       +"/"
                       +app.config['MYSQLDBNAME'] \
                       +"?charset=utf8", \
                        echo=True)

app.config['dbsession'] = sessionmaker(bind=engine)()

# register blueprint
app.register_blueprint(view)
app.register_blueprint(apiview)
app.register_blueprint(apiauthor)
app.register_blueprint(apibook)
app.register_blueprint(apiuser)
