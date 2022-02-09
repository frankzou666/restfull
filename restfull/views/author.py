from flask import jsonify,Blueprint,current_app,request,make_response
from datetime import datetime
import logging
from restfull.models.author import Author
import json
from restfull.commons.responses import response_with
from restfull.commons import responses
from restfull.commons.utils import  getFields

apiauthor = Blueprint('apiauthor', __name__, url_prefix='/myapp/api')


@apiauthor.route('/authors', methods=['GET'])
def getAuthorsAll():
    """
    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        authors = []
        results = dbsession.query(Author).all()
        if results:
            authors = [author.toJson() for author in results]
        dbsession.execute('commit')
        return response_with(response=responses.SUCCESS_200, value=authors)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiauthor.route('/authors/<int:authorid>',methods=['GET'])
def getAuthorsByID(authorid):
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        authors = []
        results = dbsession.query(Author).filter(Author.id==authorid).all()
        if results:
            authors = [author.toJson() for author in results]
        dbsession.execute('commit')
        return response_with(response=responses.SUCCESS_200, value=authors)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiauthor.route('/authors', methods=['POST'])
def createAuthor():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        authors = []
        author = Author()
        newauthor = request.get_json()
        author.first_name = newauthor.get('first_name')
        author.last_name = newauthor.get('last_name')
        author.created = datetime.now()
        dbsession.add(author)
        dbsession.execute('commit')
        dbsession.commit()
        authors.append(author)
        if len(authors) > 0:
            authors = [author.toJson() for author in authors]
        return response_with(response=responses.SUCCESS_201, value=authors)

    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiauthor.route('/authors/<int:authorid>', methods=['PUT'])
def updateAuthor(authorid):
    """
    update author first_name and last_name by authorid
    :return:
    :arg: authorid,
    """
    dbsession = current_app.config['dbsession']
    try:
        authors = []
        results = dbsession.query(Author).filter(Author.id==authorid).all()
        if len(results) == 1:
            data = {}
            author = results[0]
            newauthor = request.get_json()
            data['id'] = author.id
            if newauthor.get('first_name'):
                author.first_name = newauthor.get('first_name')
                data['first_name'] = newauthor.get('first_name')
            if newauthor.get('last_name'):
                author.last_name = newauthor.get('last_name')
                data['last_name'] = newauthor.get('last_name')
        else:
            return response_with(response=responses.SERVER_ERROR_404, value=authors)
        authors = [json.dumps(data)]
        dbsession.add(author)
        dbsession.execute('commit')
        dbsession.commit()
        return response_with(response=responses.SUCCESS_200, value=authors)
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apiauthor.route('/authors/<int:authorid>', methods=['DELETE'])
def deleteAuthor(authorid):
    """
    delete author by authorid
    :return:
    :argument:authorid
    """
    dbsession = current_app.config['dbsession']
    try:
        authors = []
        results = dbsession.query(Author).filter(Author.id == authorid).all()
        if len(results) == 1:
            data = {}
            author = results[0]
            data['id'] = author.id
        else:
            return response_with(response=responses.SERVER_ERROR_404, value=authors)
        authors = [json.dumps(data)]
        dbsession.delete(author)
        dbsession.execute('commit')
        dbsession.commit()
        return response_with(response=responses.SUCCESS_200, value=authors)
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)