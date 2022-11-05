from sqlalchemy import Column, Integer, VARCHAR, TEXT
from db import Base, session


class User(Base):
    """User in database"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(VARCHAR)
    chat_id = Column(Integer)


class Anketa(Base):
    """Anketa users"""
    __tablename__ = 'anketa'

    anketa_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(TEXT)
    rating = Column(Integer)
    user_comment = Column(TEXT)


def add_user_db(user_name, chat_id):
    query = session.query(User).order_by(User.chat_id)
    for chat in query:
        if chat_id == chat.chat_id:
            return None
        user = User(user_name=user_name, chat_id=chat_id)
        session.add(user)
        session.commit()


def add_anketa(user_name, user_id, rating, user_comment):
    print(user_name, user_id, rating, user_comment)

    anketa = Anketa(
        user_name=user_name, user_id=user_id,
        rating=rating, user_comment=user_comment
                   )

    session.add(anketa)
    session.commit()
