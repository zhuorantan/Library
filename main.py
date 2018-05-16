from flask import Flask, jsonify, request, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db_session, init_db, populate_data
from tables import *
from datetime import date, datetime, timedelta
from sqlalchemy import or_
# from gmail import send_email

app = Flask(__name__)

init_db()
# populate_data()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('books_management.html', book_locations=['图书流通室', '图书阅览室'])
        else:
            return render_template('login.html')
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        user = User.query.filter_by(id=user_id).first()
        if user:
            if user.password == password:
                login_user(user)
                user.is_authenticated = True
                db_session.commit()
                return redirect('/')
            else:
                return render_template('login.html', error='密码错误', user_id=user_id, password=password)
        else:
            return render_template('login.html', error='用户不存在', user_id=user_id, password=password)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    db_session.commit()
    return redirect('/')


@app.route('/cip_books')
@login_required
def cip_books():
    return render_template('cip_books.html', data_url='books?isbn=%s' % request.args['isbn'], index=request.args['index'])


@app.route('/cips', methods=['GET'])
@login_required
def cips():
    isbn_prefix = request.args.get('isbn_prefix', None)

    if isbn_prefix:
        cips = CIP.query.filter(CIP.isbn.startswith(isbn_prefix))
    else:
        cips = CIP.query.all()

    properties = [cip.properties() for cip in cips]

    for index in range(len(properties)):
        cip = cips[index]
        properties[index]['deletable'] = all([book.status == BookStatus.available for book in cip.books])
        properties[index]['reservable'] = all([book.status != BookStatus.available for book in cip.books])

    return jsonify(properties)


@app.route('/readers', methods=['GET'])
@login_required
def readers():
    query_text = request.args.get('query_text')

    if query_text:
        readers = Reader.query.filter(or_(Reader.id.like('%' + query_text + '%'), Reader.name.like('%' + query_text + '%')))
    else:
        readers = Reader.query.all()
    return jsonify([reader.properties() for reader in readers])


@app.route('/cip', methods=['GET'])
@login_required
def cip():
    isbn = request.args.get('isbn', None)

    cip = CIP.query.get(isbn)

    return jsonify(cip.properties())


@app.route('/books', methods=['GET'])
@login_required
def books():
    isbn = request.args['isbn']
    books = Book.query.filter(Book.cip_id == isbn)
    return jsonify([book.properties() for book in books])


@app.route('/borrowed_info', methods=['GET'])
@login_required
def borrowed_info():
    book_id = request.args['book_id']
    book = Book.query.get(book_id)
    borrows = [borrow for borrow in book.borrows if borrow.actual_return_date is None]

    if len(borrows) > 0:
        return jsonify(borrows[0].properties())
    else:
        return jsonify([])


@app.route('/reservation_info', methods=['GET'])
@login_required
def reservation_info():
    book_id = request.args['book_id']
    book = Book.query.get(book_id)

    return jsonify(book.reservation.properties())


@app.route('/librarian_info', methods=['GET'])
@login_required
def librarian_info():
    user_id = request.args['user_id']
    librarian = Librarian.query.get(user_id)

    return jsonify(librarian.properties())


@app.route('/book_entry', methods=['POST'])
@login_required
def book_entry():
    isbn = request.form['isbn']
    librarian = current_user

    cip = CIP.query.get(isbn)
    if cip is None:
        book_name = request.form['book_name']
        author = request.form['author']
        publisher = request.form['publisher']
        publish_year_month = datetime.strptime(request.form['publish_date'], '%Y-%m').date()

        cip = CIP(isbn=isbn, book_name=book_name, author=author, publisher=publisher, publish_year_month=publish_year_month, librarian=librarian)

    location = request.form['location']
    book_ids = request.form.getlist('book_id')

    status = BookStatus.available if location == '图书流通室' else BookStatus.unborrowable
    books = [Book(id=book_id, cip=cip, location=location, status=status, librarian=librarian) for book_id in book_ids]

    db_session.add_all(books)
    db_session.commit()
    return jsonify({'success': True})


@app.route('/book_borrow', methods=['POST'])
@login_required
def book_borrow():
    reader_id = request.form['reader_id']
    book_id = request.form['book_id']

    reader = Reader.query.get(reader_id)
    if len([borrow for borrow in reader.borrows if borrow.actual_return_date is None]) >= 10:
        return jsonify({'success': False})

    book = Book.query.get(book_id)
    book.status = BookStatus.borrowed

    borrow = Borrow(reader=reader, book=book, borrow_date=date.today(), excepted_return_date=datetime.strptime(request.form['deadline'], '%Y-%m-%d').date())

    if book.reservation:
        db_session.delete(book.reservation)

    db_session.add(borrow)
    db_session.commit()

    return jsonify({'success': True})


@app.route('/book_reserve', methods=['POST'])
@login_required
def book_reserve():
    reader_id = request.form['reader_id']
    isbn = request.form['isbn']

    reader = Reader.query.get(reader_id)

    cip = CIP.query.get(isbn)

    reservation = Reservation(reader=reader, cip=cip, reserve_date=date.today(), duration=request.form['duration'])

    db_session.add(reservation)
    db_session.commit()

    return jsonify({'success': True})


@app.route('/book_return', methods=['POST'])
@login_required
def book_return():
    book_id = request.form['book_id']

    book = Book.query.get(book_id)
    borrow = [borrow for borrow in book.borrows if borrow.actual_return_date is None][0]
    borrow.actual_return_date = date.today()

    pending_reservations = [reservation for reservation in book.cip.reservations if reservation.book is None]
    if len(pending_reservations) > 0:
        reservation = pending_reservations[0]
        reservation.book = book
        reservation.available_date = date.today()
        book.status = BookStatus.reserved

        message = '%s，\n    您好！\n    您预约的书《%s》可借了，请在%s之前到%s借书，否则预约将被取消。\n\n\n\n图书馆' % (reservation.reader.name, book.cip.book_name, (date.today() + timedelta(days=reservation.duration)).strftime('%Y年%m月%d日'), book.location)
        send_email(reservation.reader.email, '您预约的书%s可借了' % book.cip.book_name, message)
    else:
        book.status = BookStatus.available

    db_session.commit()

    result = {'success': True}
    delay = (borrow.actual_return_date - borrow.excepted_return_date).days
    if delay > 0:
        result['delay'] = delay

    return jsonify(result)


@app.route('/update_cip', methods=['POST'])
@login_required
def update_cip():
    isbn = request.form['isbn']
    cip = CIP.query.get(isbn)
    cip.book_name = request.form['book_name']
    cip.author = request.form['author']
    cip.publisher = request.form['publisher']
    cip.publish_year_month = datetime.strptime(request.form['publish_date'], '%Y-%m').date()

    db_session.commit()
    return jsonify({'success': True})


@app.route('/delete_cip', methods=['DELETE'])
@login_required
def delete_cip():
    isbn = request.args['isbn']
    cip = CIP.query.get(isbn)
    db_session.delete(cip)
    db_session.commit()
    return jsonify({'success': True})


@app.route('/delete_book', methods=['DELETE'])
@login_required
def delete_book():
    book_id = request.args['book_id']
    book = Book.query.get(book_id)
    db_session.delete(book)
    db_session.commit()
    return jsonify({'success': True})


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.secret_key = 'com.jerome-tan.library'
if __name__ == "__main__":
    app.config['ENV'] = 'production'
    app.run(host='0.0.0.0', debug=False)
