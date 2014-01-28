from sqlalchemy import Column, String, Integer

from settings import BaseModel


class Author(BaseModel):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    def __repr__(self):
         u'%s' % self.name
