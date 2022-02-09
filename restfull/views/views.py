

from flask import jsonify,Blueprint,current_app
from restfull.commons import responses
from restfull.commons.responses import response_with
from datetime import datetime
import logging

view = Blueprint('view', __name__)


@view.route('/')
def hello():
    """

    :return:
    """
    # print(current_app.config['APPDIR'])
    # logging.info(current_app.config['APPDIR'] + ' from logging')
    return jsonify({'datetime':datetime.now()})


@view.after_request
def add_header(response):
    return response


@view.errorhandler(400)
def badRequest(e):
    logging.error(e)
    return response_with(responses.BAD_REQUEST_400)

@view.errorhandler(404)
def notFound(e):
    logging.error(e)
    return response_with(responses.SERVER_ERROR_404)

@view.errorhandler(500)
def serverError(e):
    logging.error(e)
    return response_with(responses.SERVER_ERROR_500)