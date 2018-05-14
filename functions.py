from tables import *
from datetime import timedelta


def book_entry(isbn, book_name, author, publisher, publish_year_month, librarian_id, book_id, location):
    librarian = session.query(Librarian).filter(Librarian.id == librarian_id).first()
    cip = session.query(CIP).filter(CIP.isbn == isbn).first()
    if cip is None:
        cip = CIP(ISBN=isbn, book_name=book_name, author=author, publisher=publisher, publish_year_month=publish_year_month, books_num=1, librarian=librarian)
        session.add(cip)
    else:
        cip.books_num += 1

    state = Book_state.unborrowed if location == '图书流通室' else Book_state.can_not_be_borrowed
    book = Book(id=book_id, cip=cip, location=location, state=state, librarian=librarian)

    session.add(book)
    session.commit()


# book_entry('ISBN7-302-02368-9', '数据结构', '严蔚敏 吴伟民', '清华大学出版社', date(year=1997, month=4, day=1), 'lib0001', 'C832.5', '图书流通室')
# book_entry('ISBN7-302-14697-4', '解忧杂货店', '东野圭吾', '南海出版公司', date(year=2014, month=5, day=1), 'lib0001', 'C123.1', '图书流通室')


def borrow_book(reader_id, book_id):
    reader = session.query(Reader).filter(Reader.id == reader_id).first()
    book = session.query(Book).filter(Book.id == book_id).first()

    book.state = Book_state.borrowed
    reader.borrow_num += 1
    borrow = Borrow(reader=reader, book=book, borrow_date=date.today(), should_return_date=date.today()+timedelta(days=60))

    session.add(borrow)
    session.commit()


# borrow_book('rea0002', 'C123.1')


def reserve_book(reader_id, isbn):
    reader = session.query(Reader).filter(Reader.id == reader_id).first()
    cip = session.query(CIP).filter(CIP.isbn == isbn).first()

    reserve = Reservation(reader=reader, cip=cip, reserve_date=date.today(), reserve_deadline=date.today() + timedelta(days=10))
    session.add(reserve)
    session.commit()


# reserve_book('rea0001', 'ISBN7-302-14697-4')


def return_book(reader_id, book_id):
    reader = session.query(Reader).filter(Reader.id == reader_id).first()
    book = session.query(Book).filter(Book.id == book_id).first()
    borrow = session.query(Borrow).filter(Borrow.reader_id == reader.id, Borrow.book_id == book.id, Borrow.actual_return_date == None).first()

    borrow.actual_return_date = date.today()
    reserve = session.query(Reservation).filter(Reservation.cip_id == book.cip.ISBN, Reservation.book_id == None).first()
    if reserve is not None:
        book.state = Book_state.reserved
        reserve.book_id = book.id
    else:
        book.state = Book_state.unborrowed
    reader.borrow_num -= 1
    session.commit()


# return_book('rea0002', 'C123.1')


def clear_reserve_table():
    invalid_reserves = session.query(Reservation).filter(date.today() > Reservation.reserve_deadline).all()
    if invalid_reserves is not None:
        for invalid_reserve in invalid_reserves:
            if invalid_reserve.book_id is not None and invalid_reserve.book.state == Book_state.reserved:
                invalid_reserve.book.state = Book_state.unborrowed
            session.delete(invalid_reserve)
        session.commit()
