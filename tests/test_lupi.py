import os
import tempfile

import pytest

from lupi_app import config
from lupi_app import build_database
from lupi_app.lupi import Lupi


@pytest.fixture(scope="session")
def test_db():
    db_fd, config.app.config['SQLITE_FILE'] = tempfile.mkstemp()
    config.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + config.app.config['SQLITE_FILE']
    config.app.config['TESTING'] = True

    with config.app.test_client() as client:
        with config.app.app_context():
            build_database.build()
        yield client

    os.close(db_fd)
    os.unlink(config.app.config['SQLITE_FILE'])


def test_start_new_round(test_db):
    (data, code) = Lupi.start_new_round()
    assert code == 201
    assert data["round_id"] == 1


def test_start_new_round_409(test_db):
    (data, code) = Lupi.start_new_round()
    assert code == 409
    assert data == "There is active round."


def test_insert_vote(test_db):
    (data, code) = Lupi.insert_vote('A', 3)
    assert code == 201
    assert data["round_id"] == 1

    (data, code) = Lupi.insert_vote('B', 5)
    assert code == 201
    assert data["round_id"] == 1

    (data, code) = Lupi.insert_vote('C', 3)
    assert code == 201
    assert data["round_id"] == 1

    (data, code) = Lupi.insert_vote('D', 4)
    assert code == 201
    assert data["round_id"] == 1

    (data, code) = Lupi.insert_vote('E', 2)
    assert code == 201
    assert data["round_id"] == 1

    (data, code) = Lupi.insert_vote('F', 6)
    assert code == 201
    assert data["round_id"] == 1


def test_insert_vote_with_used_name(test_db):
    (data, code) = Lupi.insert_vote('A', 1)
    assert code == 412
    assert data == "The given name is used in this round."


def test_insert_vote_without_name(test_db):
    (data, code) = Lupi.insert_vote('', 1)
    assert code == 412
    assert data == "Name is required."


def test_insert_vote_with_invalid_number_1(test_db):
    (data, code) = Lupi.insert_vote('X', 'a')
    assert code == 412
    assert data == "Invalid number."


def test_insert_vote_with_invalid_number_2(test_db):
    (data, code) = Lupi.insert_vote('X', -1)
    assert code == 412
    assert data == "The number must be a positive integer."


def test_get_result_with_unexist_id(test_db):
    (data, code) = Lupi.get_result(11)
    assert code == 404
    assert data == "Round not found for ID: 11"


def test_get_result_with_active_round_id(test_db):
    (data, code) = Lupi.get_result(1)
    assert code == 404
    assert data == "Round result is not available for ID: 1. Please try again later!"


def test_stop_round_with_unexist_id(test_db):
    (data, code) = Lupi.stop_round(11)
    assert code == 404
    assert data == "Round not found for ID: 11"


def test_stop_round_if_has_winner(test_db):
    (data, code) = Lupi.stop_round(1)
    assert code == 200
    assert data["winner"] == "E"
    assert data["number"] == 2


def test_stop_round_with_inactive_round_id(test_db):
    (data, code) = Lupi.stop_round(1)
    assert code == 404
    assert data == "Round is not active for ID: 1"


def test_insert_vote_without_active_round(test_db):
    (data, code) = Lupi.insert_vote('A', 1)
    assert code == 404
    assert data == "No active round."


def test_start_new_round_2(test_db):
    (data, code) = Lupi.start_new_round()
    assert code == 201
    assert data["round_id"] == 2


def test_insert_vote_draw(test_db):
    (data, code) = Lupi.insert_vote('A', 3)
    assert code == 201
    assert data["round_id"] == 2

    (data, code) = Lupi.insert_vote('B', 5)
    assert code == 201
    assert data["round_id"] == 2

    (data, code) = Lupi.insert_vote('C', 3)
    assert code == 201
    assert data["round_id"] == 2

    (data, code) = Lupi.insert_vote('D', 5)
    assert code == 201
    assert data["round_id"] == 2


def test_stop_round_if_draw(test_db):
    (data, code) = Lupi.stop_round(2)
    assert code == 200
    assert data["winner"] == ""
    assert data["number"] == -1


def test_get_result_if_has_winner(test_db):
    (data, code) = Lupi.get_result(1)
    assert code == 200
    assert data["winner"] == "E"
    assert data["number"] == 2


def test_get_result_if_draw(test_db):
    (data, code) = Lupi.get_result(2)
    assert code == 200
    assert data["winner"] == ""
    assert data["number"] == -1


def test_get_rounds(test_db):
    (data, code) = Lupi.get_rounds()
    assert code == 200
    assert len(data) == 2
    assert data[0]["round_id"] == 1
    assert data[0]["num_of_participants"] == 6
    assert data[1]["round_id"] == 2
    assert data[1]["num_of_participants"] == 4


def test_get_stat_with_unexist_id(test_db):
    (data, code) = Lupi.get_stat(5)
    assert code == 404
    assert data == "Round not found for ID: 5"


def test_get_stat(test_db):
    (data, code) = Lupi.get_stat(1)
    assert code == 200
    assert len(data) == 5
    assert data[0]["number"] == 2
    assert data[0]["count"] == 1
    assert data[1]["number"] == 3
    assert data[1]["count"] == 2
    assert data[2]["number"] == 4
    assert data[2]["count"] == 1
    assert data[3]["number"] == 5
    assert data[3]["count"] == 1
    assert data[4]["number"] == 6
    assert data[4]["count"] == 1


def test_start_new_round_3(test_db):
    (data, code) = Lupi.start_new_round()
    assert code == 201
    assert data["round_id"] == 3


def test_stop_round_if_no_vote(test_db):
    (data, code) = Lupi.stop_round(3)
    assert code == 200
    assert data["winner"] == ""
    assert data["number"] == -1
