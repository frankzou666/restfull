

from flask import jsonify,Blueprint,current_app
from datetime import datetime
import logging

view = Blueprint('view', __name__)


@view.route('/')
def hello():
    """

    :return:
    """
    #print(current_app.config['APPDIR'])
    #logging.info(current_app.config['APPDIR'] + ' from logging')
    return jsonify({'datetime':datetime.now()})