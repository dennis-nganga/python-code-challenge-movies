from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String())
    salary = Column(Integer())

    actor_id = Column(Integer, ForeignKey('actors.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))

    actor = relationship("Actor", backref="roles")
    movie = relationship("Movie", backref="roles")

    def __repr__(self):
        return f'Role: {self.character_name}'


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f'Actor: {self.name}'


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String())
    box_office_earnings = Column(Integer())

    def __repr__(self):
        return f'Movie: {self.title}'
