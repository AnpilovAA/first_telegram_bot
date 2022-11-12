from mock_data import MockData
from models import User, add_user_db


def test_get_session(session):
    assert session.execute('SELECT 2').scalar() == 2


def test_session_user_table(session):
    assert session.execute('SELECT COUNT(*) FROM users').scalar() == 0


def test_mocked_session_user_table(mocked_session):
    user_data = mocked_session.execute("SELECT * FROM users;").first()
    print(user_data[0])
    raw_data = MockData.USER_DATA[0]
    assert user_data[0] == raw_data['users_id']
    assert user_data[1] == raw_data['user_name']
    assert user_data[2] == raw_data['user_id']


def test_mocked_session_user_model(mocked_session):
    user = mocked_session.query(User).filter_by(users_id=1).first()
    raw_data = MockData.USER_DATA[0]
    assert user.user_name == raw_data['user_name']
    assert user.user_id == raw_data['user_id']


def test_add_user_db_is_none(mocked_session, effective_user):
    user_exist = mocked_session.query(User).filter_by(
        user_id=effective_user.user_id).first()
    assert user_exist is None


def test_add_user_db(mocked_session, effective_user):
    user_exist = mocked_session.query(User).filter_by(
        user_id=effective_user.user_id).first()
    user = add_user_db(effective_user.user_name, effective_user.user_id)
    assert user == user_exist
