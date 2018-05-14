from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


class BookStatus(enum.Enum):
    borrowed = 1
    available = 2
    reserved = 3
    unborrowable = 4

    def name(self):
        if self == BookStatus.borrowed:
            return "已借出"
        elif self == BookStatus.available:
            return "未借出"
        elif self == BookStatus.reserved:
            return "已预约"
        elif self == BookStatus.unborrowable:
            return "不外借"


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(String(30), primary_key=True)
    name = Column(String(30))
    password = Column(String(30))

    type = Column(String(30))

    is_authenticated = Column(BOOLEAN, default=False)
    is_active = True
    is_anonymous = False

    def get_id(self):
        return self.id

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Librarian(User):
    cips = relationship('CIP', back_populates='librarian')
    books = relationship('Book', back_populates='librarian')

    __mapper_args__ = {
        'polymorphic_identity': 'librarian'
    }

    def properties(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }


class Reader(User):
    tel = Column(String(30))
    email = Column(String(30))

    borrows = relationship('Borrow', back_populates='reader')
    reservations = relationship('Reservation', back_populates='reader')

    __mapper_args__ = {
        'polymorphic_identity': 'reader'
    }

    def properties(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'tel': self.tel,
            'email': self.email,
            'borrows': [borrow.properties() for borrow in self.borrows]
        }


class CIP(Base):
    __tablename__ = 'cip'

    isbn = Column(String(30), primary_key=True)
    book_name = Column(String(30))
    author = Column(String(30))
    publisher = Column(String(30))
    publish_year_month = Column(Date)
    librarian_id = Column(String(30), ForeignKey('user.id'))

    librarian = relationship('Librarian', back_populates='cips')
    books = relationship('Book', back_populates='cip')
    reservations = relationship('Reservation', back_populates='cip')

    def books_num(self):
        return len(self.books)

    def properties(self):
        return {
            'isbn': self.isbn,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher,
            'publish_date': self.publish_year_month.strftime('%Y-%m'),
            'books': [book.properties() for book in self.books],
            'book_ids': ';'.join(book.id for book in self.books),
            'librarian_name': self.librarian.name,
            'available_count': len([book for book in self.books if book.status == BookStatus.available])
        }


class Book(Base):
    __tablename__ = 'book'

    id = Column(String(30), primary_key=True)
    cip_id = Column(String(30), ForeignKey('cip.isbn'))
    location = Column(String(30))
    status = Column(Enum(BookStatus))
    librarian_id = Column(String(30), ForeignKey('user.id'))

    cip = relationship('CIP', back_populates='books')
    librarian = relationship('Librarian', back_populates='books')
    borrows = relationship('Borrow', back_populates='book')
    reservation = relationship('Reservation', back_populates='book', uselist=False)

    def properties(self):
        properties = {
            'id': self.id,
            'cip_id': self.cip_id,
            'location': self.location,
            'status': self.status.name(),
            'librarian_name': self.librarian.name
        }

        if self.reservation:
            properties['reservation'] = self.reservation.properties()

        return properties


class Borrow(Base):
    __tablename__ = 'borrow'

    reader_id = Column(String(30), ForeignKey('user.id'), primary_key=True)
    book_id = Column(String(30), ForeignKey('book.id'), primary_key=True)
    borrow_date = Column(Date, primary_key=True)
    excepted_return_date = Column(Date)
    actual_return_date = Column(Date, default=None)

    reader = relationship('Reader', back_populates='borrows')
    book = relationship('Book', back_populates='borrows')

    def properties(self):
        properties = {
            'reader_id': self.reader_id,
            'book_id': self. book_id,
            'borrow_date': self.borrow_date.isoformat(),
            'expected_return_date': self.excepted_return_date.isoformat()
        }

        if self.actual_return_date:
            properties['actual_return_date'] = self.actual_return_date.isoformat()

        return properties


class Reservation(Base):
    __tablename__ = 'reservation'

    reader_id = Column(String(30), ForeignKey('user.id'), primary_key=True)
    cip_id = Column(String(30), ForeignKey('cip.isbn'), primary_key=True)
    book_id = Column(String(30), ForeignKey('book.id'))
    reserve_date = Column(Date, primary_key=True)
    duration = Column(Integer)

    reader = relationship('Reader', back_populates='reservations')
    cip = relationship('CIP', back_populates='reservations')
    book = relationship('Book', back_populates='reservation')

    def properties(self):
        return {
            'reader_id': self.reader_id,
            'cip_id': self.cip_id,
            'reserve_date': self.reserve_date.isoformat(),
            'duration': self.duration
        }
