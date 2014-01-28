from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from settings import BaseModel


authors = Table('authors', BaseModel.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)


class Book(BaseModel):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    authors = relationship('Author', secondary=authors,
                           backref=backref('books', lazy='dynamic'))

    def __repr__(self):
         u'%s' % self.name
