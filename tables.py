from sqlalchemy import Column, Integer, String, Float, Enum, Date, ForeignKey, BOOLEAN, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum


class BookState(enum.Enum):
    borrowed = 1
    unborrowed = 2
    reserved = 3
    can_not_be_borrowed = 4


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(String(30), primary_key=True)
    name = Column(String(30))
    password = Column(String(30))

    type = Column(String(30))

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
    borrow_num = Column(Integer)

    borrows = relationship('Borrow', back_populates='reader')
    reserves = relationship('Reserve', back_populates='reader')

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
            'borrow_num': self.borrow_num
        }


class CIP(Base):
    __tablename__ = 'cip'

    isbn = Column(String(30), primary_key=True)
    book_name = Column(String(30))
    author = Column(String(30))
    publisher = Column(String(30))
    publish_year_month = Column(Date)
    books_num = Column(Integer)
    librarian_id = Column(String(30), ForeignKey('user.id'))

    librarian = relationship('Librarian', back_populates='cips')
    books = relationship('Book', back_populates='cip')
    reserves = relationship('Reserve', back_populates='cip')

    def properties(self):
        return {
            'id': self.isbn,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher,
            'publish_year_month': self.publish_year_month.isoformat(),
            'quantity': self.books_num,
            'librarian_name': self.librarian.name
        }


class Book(Base):
    __tablename__ = 'book'

    id = Column(String(30), primary_key=True)
    cip_id = Column(String(30), ForeignKey('cip.isbn'))
    location = Column(String(30))
    state = Column(Enum(BookState))
    librarian_id = Column(String(30), ForeignKey('user.id'))

    cip = relationship('CIP', back_populates='books')
    librarian = relationship('Librarian', back_populates='books')
    borrows = relationship('Borrow', back_populates='book')
    reserved = relationship('Reserve', back_populates='book')

    def properties(self):
        return {
            'id': self.id,
            'cip_id': self.cip_id,
            'location': self.location,
            'state': self.getstate(),
            'librarian_id': self.librarian_id
        }

    def getstate(self):
        if self.state == BookState.borrowed:
            return "已借出"
        elif self.state == BookState.unborrowed:
            return "未借出"
        elif self.state == BookState.reserved:
            return "已预约"
        else:
            return "不外借"


class Borrow(Base):
    __tablename__ = 'borrow'

    reader_id = Column(String(30), ForeignKey('user.id'), primary_key=True)
    book_id = Column(String(30), ForeignKey('book.id'), primary_key=True)
    borrow_date = Column(Date, primary_key=True)
    should_return_date = Column(Date)
    actual_return_date = Column(Date)

    reader = relationship('Reader', back_populates='borrows')
    book = relationship('Book', back_populates='borrows')

    def properties(self):
        return {
            'reader_id': self.reader_id,
            'book_id': self. book_id,
            'borrow_date': self.borrow_date.isoformat(),
            'should_return_date': self.should_return_date.isoformat(),
            'actual_return_date': self.actual_return_date.isoformat()
        }


class Reserve(Base):
    __tablename__ = 'reserve'

    reader_id = Column(String(30), ForeignKey('user.id'), primary_key=True)
    cip_id = Column(String(30), ForeignKey('cip.isbn'), primary_key=True)
    reserve_date = Column(Date, primary_key=True)
    reserve_deadline = Column(Date)
    book_id = Column(String(30), ForeignKey('book.id'))

    reader = relationship('Reader', back_populates='reserves')
    cip = relationship('CIP', back_populates='reserves')
    book = relationship('Book', back_populates='reserved')

    def properties(self):
        return {
            'reader_id': self.reader_id,
            'cip_id': self.cip_id,
            'reserve_date': self.reserve_date.isoformat(),
            'reserve_deadline': self.reserve_deadline.isoformat(),
            'book_id': self.book_id
        }
