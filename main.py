from flask import Flask, jsonify, request
from database import db_session, init_db
from tables import *
from datetime import date

app = Flask(__name__)

init_db()

# librarian1 = Librarian(id='lib0001', name='张三', password='lib0001')
# librarian2 = Librarian(id='lib0002', name='李四', password='lib0002')
# librarian3 = Librarian(id='lib0003', name='王五', password='lib0003')
#
# reader1 = Reader(id='rea0001', name='李明', password='rea0001', tel='18800201111', email='18800201111@163.com', borrow_num=0)
# reader2 = Reader(id='rea0002', name='刘晓明', password='rea0002', tel='18800202222', email='18800202222@163.com', borrow_num=0)
# reader3 = Reader(id='rea0003', name='张颖', password='rea0003', tel='18800203333', email='18800203333@163.com', borrow_num=0)
#
# cip1 = CIP(isbn='ISBN7-302-02368-9', book_name='数据结构', author='严蔚敏 吴伟民', publisher='清华大学出版社', publish_year_month=date(year=1997, month=4, day=1), books_num=4, librarian=librarian1)
# cip2 = CIP(isbn='ISBN7-302-02357-1', book_name='数据库使用教程', author='董建全', publisher='清华大学出版社', publish_year_month=date(year=2016, month=4, day=1), books_num=2, librarian=librarian1)
#
# book1 = Book(id='C832.1', cip=cip1, location='图书流通室', state=BookState.unborrowed, librarian=librarian1)
# book2 = Book(id='C832.2', cip=cip1, location='图书流通室', state=BookState.unborrowed, librarian=librarian1)
# book3 = Book(id='C832.3', cip=cip1, location='图书流通室', state=BookState.unborrowed, librarian=librarian1)
# book4 = Book(id='C832.4', cip=cip1, location='图书阅览室', state=BookState.can_not_be_borrowed, librarian=librarian1)
#
# book5 = Book(id='C357.1', cip=cip2, location='图书流通室', state=BookState.unborrowed, librarian=librarian1)
# book6 = Book(id='C357.2', cip=cip2, location='图书流通室', state=BookState.unborrowed, librarian=librarian1)
#
# db_session.add_all([librarian1, librarian2, librarian2,
#                     reader1, reader2, reader3,
#                     cip1, cip2,
#                     book1, book2, book3, book4, book5, book6])
# db_session.commit()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/cip', methods=['GET', 'OPTIONS'])
def cip():
    cips = db_session.query(CIP).all()
    return jsonify({
        'rows': [cip.properties() for cip in cips],
        'total': 500
    })


@app.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id', None)
    password = request.json.get('password', None)

    if not (user_id and password):
        return jsonify({'success': False})

    user = User.query.filter(User.id == user_id).first()

    if not user or user.password != password:
        return jsonify({'success': False})

    return jsonify({
        'success': True,
        'type': user.type,
        'user': user.properties()
    })


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.run(host='0.0.0.0')
