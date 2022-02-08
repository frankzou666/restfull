

from flask import Flask
from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from restfull.views.views import view
from restfull.views.api import apiview
import os
import pymysql


#new app
app = Flask(__name__)
app.config.from_object('config')
app.config['APPDIR'] = os.getcwd()


#config logger
if app.config['PROD']:
    logging.basicConfig(level=app.config['LOGLEVEL'],
                        format='%(levelname)s:%(asctime)s-%(filename)s-%(module)s-%(lineno)d:%(message)s',
                        filename=os.path.join(app.config['APPDIR'],'myapp','logs','app.log'))
else:
    logging.basicConfig(level=app.config['LOGLEVEL'],
                        format='%(levelname)s:%(asctime)s-%(filename)s-%(module)s-%(lineno)d:%(message)s'
                        )

#create dbengine

engine = create_engine( "mysql+pymysql://"+app.config['MYSQLUSER']+":" \
                       +app.config['MYSQLPWD']+"@"
                       +app.config['MYSQLHOST']+":" \
                       +str(app.config['MYSQLPORT']) \
                       +"/"
                       +app.config['MYSQLDBNAME'] \
                       +"?charset=utf8", \
                        echo=True)

app.config['dbsession'] = sessionmaker(bind=engine)()



#register buleprint
app.register_blueprint(view)
app.register_blueprint(apiview)

