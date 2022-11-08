from sqlalchemy import Boolean, Column, Integer, VARCHAR, TEXT
from db import Base, session


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


def add_user_db(user_name, chat_id):
    query = session.query(User).order_by(User.user_id)
    for chat in query:
        if chat_id == chat.user_id:
            return None

    user = User(user_name=user_name, user_id=chat_id)
    return add_to_database(user)


def add_anketa(user_name, user_id, rating, user_comment):
    anketa = Anketa(
            user_name=user_name, user_id=user_id,
            rating=rating, user_comment=user_comment
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


def add_to_database(table):
    try:
        session.add(table)
    except Exception as ex:
        session.rollback()
        print(repr(ex))
        raise
    else:
        session.commit()


def get_subscribe():
    return session.query(Subscribes).filter(
            Subscribes.subscribe == True
            ).all()
