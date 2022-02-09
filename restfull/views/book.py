from flask import jsonify,Blueprint,current_app,request,make_response
from datetime import datetime
import logging
from restfull.models.book import Book
import json
from restfull.commons.responses import response_with
from restfull.commons import responses
from restfull.commons.utils import getFields
from flask_jwt_extended import jwt_required

apibook = Blueprint('apibook', __name__,url_prefix='/myapp/api')


@apibook.route('/books', methods=['GET'])
@jwt_required()
def getBooksAll():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        books = []
        results = dbsession.query(Book).all()
        if results:
            books = [book.toJson() for book in results]
            books = getFields(datas=books, items=['id', 'title', 'year'])
        dbsession.execute('commit')
        return response_with(response=responses.SUCCESS_200, value=books)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apibook.route('/books/<int:bookid>',methods=['GET'])
def getBooksByID(bookid):
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        books = []
        results = dbsession.query(Book).filter(Book.id==bookid).all()
        if results:
            books = [book.toJson() for book in results]
        dbsession.execute('commit')
        return response_with(response=responses.SUCCESS_200, value=books)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apibook.route('/books', methods=['POST'])
def createBook():
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        books = []
        book = Book()
        newbook = request.get_json()
        book.title = newbook.get('title')
        book.year = newbook.get('year')
        dbsession.add(book)
        dbsession.execute('commit')
        dbsession.commit()
        books.append(book)
        if len(books) > 0:
            books = [book.toJson() for book in books]
        return response_with(response=responses.SUCCESS_201, value=books)

    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)



@apibook.route('/books/<int:bookid>', methods=['POST'])
def updateBook(bookid):
    """

    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        results = dbsession.query(Book).filter(Book.id==bookid).all()
        if len(results) == 1:
            newbook = request.get_json()
            book = results[0]
            if newbook.get('first_name'):
                book.first_name = newbook.get('first_name')
            if newbook.get('first_name'):
                book.first_name = newbook.get('first_name')
        dbsession.execute('commit')
        books = [book.toJson() for book in results]
        return response_with(response=responses.SUCCESS_200, value=books)
    except Exception as e:
        dbsession.execute('rollback')
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)


@apibook.route('/books/<int:bookid>', methods=['DELETE'])
def deleteBook(bookid):
    """
    delete book
    :return:
    """
    dbsession = current_app.config['dbsession']
    try:
        results = dbsession.query(Book).filter(Book.id==bookid).all()
        if len(results) == 1:
            book = results[0]
            dbsession.delete(book)
        dbsession.execute('commit')
        dbsession.commit()
        books = [json.dumps({"id": bookid})]
        return response_with(response=responses.SUCCESS_200, value=books)
    except Exception as e:
        dbsession.execute('rollback')
        dbsession.rollback()
        logging.error(e.args)
        return response_with(response=responses.SERVER_ERROR_500)