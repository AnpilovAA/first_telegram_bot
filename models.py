from sqlalchemy import Boolean, Column, Integer, VARCHAR, TEXT
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.functions import sum
from db import Base, session
# import os


class User(Base):
    """User in database"""
    __tablename__ = 'users'

    users_id = Column(Integer, primary_key=True)
    user_name = Column(VARCHAR)
    user_id = Column(Integer)

    def __repr__(self) -> str:
        return f'{self.user_id}, {self.user_name}'


class Anketa(Base):
    """Anketa users"""
    __tablename__ = 'anketa'

    anketa_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(TEXT)
    rating = Column(Integer)
    user_comment = Column(TEXT)

    def __repr__(self) -> str:
        return f'{self.user_id}, {self.user_name}, {self.user_comment}\
                 {self.rating}'


class Subscribes(Base):
    """Subs users"""
    __tablename__ = 'subscribes'

    subscribe_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    subscribe = Column(Boolean)

    def __repr__(self) -> str:
        return f'{self.user_id}, {self.subscribe}'


class UsersVotes(Base):
    """Users vote"""
    __tablename__ = 'users_votes'

    users_votes_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    image_name = Column(TEXT)
    vote = Column(Integer)

    def __repr__(self) -> str:
        return 'User_id {}, image {}, vote {}'.format(
            self.user_id, self.image_name, self.vote)


def add_user_db(user_name, chat_id):
    query = session.query(User).order_by(User.user_id)
    for chat in query:
        if chat_id == chat.user_id:
            return None

    user = User(user_name=user_name, user_id=chat_id)
    return add_to_database(user)


def add_anketa(user_name, user_id, rating, user_comment):
    anketa = Anketa(
            user_name=user_name,
            user_id=user_id,
            rating=rating,
            user_comment=user_comment
            )

    return add_to_database(anketa)


def subscribe_user(user_id, subscribe):
    query = session.query(Subscribes).order_by(Subscribes.user_id,
                                               Subscribes.subscribe)
    for user in query:
        if user.user_id == user_id and user.subscribe == subscribe:
            return None
        elif user.user_id == user_id and user.subscribe != subscribe:
            new_status = subscribe
            return update_subscribe(user_id, new_status)

    new_subscribes = Subscribes(user_id=user_id, subscribe=subscribe)
    return add_to_database(new_subscribes)


def update_subscribe(user_id, new_status):
    try:
        update_query = session.query(Subscribes).filter(
            Subscribes.user_id == user_id).one()
        update_query.subscribe = new_status
    except Exception as ex:
        session.rollback()
        print(repr(ex))
        raise
    else:
        session.commit()


def get_subscribe():
    return session.query(Subscribes
                         ).filter(
                                    Subscribes.subscribe == True
                          ).all()


def check_vote(func):
    def wrapper(*args, **kwargs):

        try:
            query = session.query(UsersVotes).filter_by(
                user_id=args[0], image_name=args[1]
            ).one()

            if args[0] == query.user_id and args[1] == query.image_name:
                return True

        except NoResultFound as ex:
            print(ex)

        func(*args, **kwargs)
    return wrapper


@check_vote
def add_vote(user_id, image, vote):
    voice = UsersVotes(
        user_id=user_id,
        image_name=image,
        vote=vote
    )
    return add_to_database(voice)


def check_user_vote(user_id, image):
    try:
        query = session.query(UsersVotes).filter_by(
                    user_id=user_id, image_name=image
        ).one()
        if query.user_id == user_id and query.image_name == image:
            return True
    except Exception as ex:
        print(repr(ex))
    return False


def rating(image):
    try:
        query = session.query(sum(UsersVotes.vote)
                              ).filter_by(image_name=image
                                          ).group_by(UsersVotes.vote,
                                                     UsersVotes.image_name
                                                     ).all()
    except Exception as ex:
        print('\n', ex)
    else:
        image_rating = query[0][0]
        if image_rating is not None:
            return image_rating
        return None


def add_to_database(table):
    try:
        session.add(table)
    except Exception as ex:
        session.rollback()
        print(repr(ex))
        raise
    else:
        session.commit()
