from flask import jsonify,Blueprint,current_app,request,make_response
from datetime import datetime
import logging
from restfull.models.user import User
import json
from restfull.commons.responses import response_with
from restfull.commons import responses
from restfull.commons.utils import  getFields
from flask_jwt_extended import create_access_token

apiuser = Blueprint('apiuser', __name__, url_prefix='/myapp/api/users')


@apiuser.route('/users', methods=['GET'])
def getUsersAll():
    """
    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        users = []
        results = dbsession.query(User).all()
        if results:
            users = [user.toJson() for user in results]
        dbsession.execute('commit')
        return response_with(response=responses.SUCCESS_200, value=users)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiuser.route('/login', methods=['POST'])
def loginUser():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        users = []
        data = request.get_json()
        results = dbsession.query(User).filter(User.username==data.get('username')).all()
        dbsession.execute('commit')
        dbsession.commit()
        if len(results) == 1:
            user = results[0]
            if User.verifyPassword(data.get('password'),user.password):
                accesstoken = create_access_token(data.get('username'))

                value = json.dumps({'access_token': accesstoken, 'message': 'logined as {}'.format(data.get('username'))})
                return response_with(response=responses.SUCCESS_200, value= value)
            else:
                return response_with(response=responses.SERVER_ERROR_404)

        else:
            return response_with(response=responses.SERVER_ERROR_404)


    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiuser.route('/', methods=['POST'])
def createUser():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        users = []
        user = User()
        newuser = request.get_json()
        user.username = newuser.get('username')
        user.password = User.generatePassword(newuser.get('password'))
        user.created = datetime.now()
        dbsession.add(user)
        dbsession.execute('commit')
        dbsession.commit()
        users.append(user)
        if len(users) > 0:
            users = [user.toJson() for user in users]
            users = getFields(datas=users, items=['id', 'username', 'created'])

        return response_with(response=responses.SUCCESS_201, value=users)

    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiuser.route('/users/<int:userid>', methods=['PUT'])
def updateUser(userid):
    """
    update user first_name and last_name by userid
    :return:
    :arg: userid,
    """
    dbsession = current_app.config['dbsession']
    try:
        users = []
        results = dbsession.query(User).filter(User.id==userid).all()
        if len(results) == 1:
            data = {}
            user = results[0]
            newuser = request.get_json()
            data['id'] = user.id
            if newuser.get('first_name'):
                user.first_name = newuser.get('first_name')
                data['first_name'] = newuser.get('first_name')
            if newuser.get('last_name'):
                user.last_name = newuser.get('last_name')
                data['last_name'] = newuser.get('last_name')
        else:
            return response_with(response=responses.SERVER_ERROR_404, value=users)
        users = [json.dumps(data)]
        dbsession.add(user)
        dbsession.execute('commit')
        dbsession.commit()
        return response_with(response=responses.SUCCESS_200, value=users)
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiuser.route('/users/<int:userid>', methods=['DELETE'])
def deleteUser(userid):
    """
    delete user by userid
    :return:
    :argument:userid
    """
    dbsession = current_app.config['dbsession']
    try:
        users = []
        results = dbsession.query(User).filter(User.id == userid).all()
        if len(results) == 1:
            data = {}
            user = results[0]
            data['id'] = user.id
        else:
            return response_with(response=responses.SERVER_ERROR_404, value=users)
        users = [json.dumps(data)]
        dbsession.delete(user)
        dbsession.execute('commit')
        dbsession.commit()
        return response_with(response=responses.SUCCESS_200, value=users)
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)