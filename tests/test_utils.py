from utils import get_bot_number, play_random_numbers


def test_get_bot_number():
    user_number = 10

    assert (
            user_number - 10
            ) <= get_bot_number(user_number) <= (
                user_number + 10
                )


def test_play_random_numbers_win():
    user_number = 10
    bot_number = 5

    assert play_random_numbers(
                    user_number, bot_number
        ) == f"Your number is {user_number},\
            my number is {bot_number}, you win"


def test_play_random_numbers_drow():
    user_number = 10
    bot_number = 10

    assert play_random_numbers(
        user_number, bot_number
        ) == f'Drow your number is {user_number},\
            my number is {bot_number}, you loose'


def test_play_random_numbers_lose():
    user_number = 5
    bot_number = 10

    assert play_random_numbers(
        user_number, bot_number
    ) == f'Your number is {user_number},\
            my number is {bot_number}, you lose'
