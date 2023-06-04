from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Actor, Movie, Role
from datetime import datetime

engine = create_engine('sqlite:///movies.db')
Session = sessionmaker(bind=engine)
session = Session()

# Object Relationship Methods

# Role methods
def role_actor(self):
    return session.query(Actor).filter_by(id=self.actor_id).first()

def role_movie(self):
    return session.query(Movie).filter_by(id=self.movie_id).first()

Role.actor = property(role_actor)
Role.movie = property(role_movie)

# Movie methods
def movie_roles(self):
    return session.query(Role).filter_by(movie_id=self.id).all()

def movie_actors(self):
    actors = session.query(Actor).join(Role).filter(Role.movie_id == self.id).all()
    return actors

Movie.roles = property(movie_roles)
Movie.actors = property(movie_actors)

# Actor methods
def actor_roles(self):
    return session.query(Role).filter_by(actor_id=self.id).all()

def actor_movies(self):
    movies = session.query(Movie).join(Role).filter(Role.actor_id == self.id).all()
    return movies

Actor.roles = property(actor_roles)
Actor.movies = property(actor_movies)

# Aggregate and Relationship Methods

# Role methods
def role_credit(self):
    actor_name = self.actor.name
    return f"{self.character_name}: Played by {actor_name}"

Role.credit = property(role_credit)

# Movie methods
def movie_cast_role(self, actor, character_name, salary):
    role = Role(actor_id=actor.id, movie_id=self.id, character_name=character_name, salary=salary)
    session.add(role)
    session.commit()

def movie_all_credits(self):
    credits = [role.credit for role in self.roles]
    return credits

def movie_fire_actor(self, actor):
    role = session.query(Role).filter_by(movie_id=self.id, actor_id=actor.id).first()
    if role:
        session.delete(role)
        session.commit()

Movie.cast_role = movie_cast_role
Movie.all_credits = property(movie_all_credits)
Movie.fire_actor = movie_fire_actor

# Actor methods
def actor_total_salary(self):
    total_salary = sum(role.salary for role in self.roles)
    return total_salary

def actor_blockbusters(self):
    movies = session.query(Movie).join(Role).filter(Role.actor_id == self.id, Movie.box_office_earnings > 50000000).all()
    return movies

@classmethod
def actor_most_successful(cls):
    actors = session.query(Actor).all()
    actor_with_highest_salary = max(actors, key=lambda actor: actor.total_salary())
    return actor_with_highest_salary

Actor.total_salary = property(actor_total_salary)
Actor.blockbusters = property(actor_blockbusters)
Actor.most_successful = actor_most_successful

actor1 = Actor(name="Actor 1")
actor2 = Actor(name="Actor 2")
movie1 = Movie(title="Movie 1", box_office_earnings=100000000)
movie2 = Movie(title="Movie 2", box_office_earnings=50000000)

# Add the instances to the session
session.add(actor1)
session.add(actor2)
session.add(movie1)
session.add(movie2)
session.commit()