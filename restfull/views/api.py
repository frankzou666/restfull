from flask import jsonify,Blueprint,current_app,request,make_response
from datetime import datetime
import logging
from restfull.models.t1 import T1
import json

apiview = Blueprint('apiview', __name__,url_prefix='/myapp/api')


@apiview.route('/users',methods=['GET'])
def getUsersAll():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    users = []
    httpcode = 500
    try:
        users = dbsession.query(T1).all()
        users = [user.toJson() for user in users]
        dbsession.execute('commit')
        httpcode = 200
    except Exception as e:
        dbsession.execute('rollback')
        httpcode = 500
        logging.error(e.args)

    return make_response(jsonify({'datetime': datetime.now(),'data':users}),httpcode)


@apiview.route('/users/<id>',methods=['GET'])
def getUsersByID(id):
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    users = []
    httpcode = 500
    try:
        users = dbsession.query(T1).filter(T1.id == id).all()
        users = [user.toJson() for user in users]
        dbsession.execute('commit')
        httpcode = 200
    except Exception as e:
        dbsession.execute('rollback')
        httpcode = 500
        logging.error(e.args)

    return make_response(jsonify({'datetime': datetime.now(),'data':users}),httpcode)

@apiview.route('/users',methods=['POST'])
def createUser():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    users = []
    httpcode = 500
    try:
        user = T1()
        user.username = request.get_json()['username']
        dbsession.add(user)
        dbsession.execute('commit')
        dbsession.commit()
        users.append(user)
        httpcode = 201
        if len(users) > 0:
            users = [user.toJson() for user in users]

    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        httpcode = 500

    return make_response(jsonify({'datetime': datetime.now(),'data':users}),httpcode)


@apiview.route('/users',methods=['DELETE'])
def deleteUser():
    """
     delete user from id
    :return:
    """
    dbsession = current_app.config['dbsession']
    users = []
    httpcode = 500
    try:
        userid = request.get_json()['id']
        users = dbsession.query(T1).filter(T1.id==userid).all()
        if len(users) == 1:
            user = users[0]
            dbsession.delete(user)
            httpcode = 200
            users = [{"id":json.loads(user.toJson())["id"]} for user in users]
        elif  len(users) == 0:
            httpcode = 422
        else:
            httpcode = 422
        dbsession.execute('commit')
        dbsession.commit()
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args.__str__())
        httpcode = 500

    return make_response(jsonify({'datetime': datetime.now(),'data':users}),httpcode)