import sys
import logging
from datetime import datetime
from sqlalchemy import func
from lupi_app.config import db
from lupi_app.models import Round, Vote


class Lupi:
    @staticmethod
    def start_new_round():
        if Round.query.filter(Round.end_ts.is_(None)).count() > 0:
            return "There is active round.", 409
        new_round = Round()

        try:
            db.session.add(new_round)
            db.session.commit()
        except:
            logging.error(f"Unexpected error: {sys.exc_info()[0]}")
            return "Internal server error. Please try again later.", 500

        return {
            "round_id": new_round.round_id
        }, 201

    @staticmethod
    def stop_round(round_id):
        round = Round.query.filter(Round.round_id == round_id).one_or_none()

        if round is None:
            return f"Round not found for ID: {round_id}", 404

        if round.end_ts is not None:
            return f"Round is not active for ID: {round_id}", 404

        winner = None

        least_number = db.session.query(Vote.number, func.count(Vote.number).label('count')).filter(Vote.round_id == round_id).group_by(Vote.number).order_by(Vote.number).all()
        for ln in least_number:
            if ln.count == 1:
                # current number is unique
                winner = Vote.query.filter(Vote.round_id == round_id, Vote.number == ln.number).one_or_none()
                break

        round.end_ts = datetime.now()
        if winner:
            round.winner = winner.vote_id

        try:
            db.session.merge(round)
            db.session.commit()
        except:
            logging.error(f"Unexpected error: {sys.exc_info()[0]}")
            return "Internal server error. Please try again later.", 500

        return {
            "winner": winner.name if winner else "",
            "number": winner.number if winner else -1
        }, 200

    @staticmethod
    def insert_vote(name, number):
        if len(name) < 1:
            return "Name is required.", 412

        try:
            number = int(number)
        except ValueError:
            return "Invalid number.", 412

        if number < 1:
            return "The number must be a positive integer.", 412

        active_round_id = Lupi.get_active_round_id()

        if active_round_id is None:
            return "No active round.", 404

        if Vote.query.filter(Vote.round_id == active_round_id, Vote.name == name).one_or_none() is not None:
            return "The given name is used in this round.", 412

        new_vote = Vote(
            round_id=active_round_id,
            name=name,
            number=number
        )

        try:
            db.session.add(new_vote)
            db.session.commit()
        except:
            logging.error(f"Unexpected error: {sys.exc_info()[0]}")
            return "Internal server error. Please try again later.", 500

        return {
            "round_id": active_round_id
        }, 201


    @staticmethod
    def get_result(round_id):
        round = Round.query.filter(Round.round_id == round_id).one_or_none()

        if round is None:
            return f"Round not found for ID: {round_id}", 404

        if round.end_ts is None:
            return f"Round result is not available for ID: {round_id}. Please try again later!", 404

        winner = Vote.query.filter(Vote.vote_id == round.winner).one_or_none()

        return {
                   "winner": winner.name if winner else "",
                   "number": winner.number if winner else -1
               }, 200


    @staticmethod
    def get_rounds():
        rounds = Round.query.order_by(Round.round_id).all()

        return [
            {
                "round_id": r.round_id,
                "start_timestamp": r.start_ts.strftime("%Y-%d-%mT%H:%M:%S.%f"),
                "stop_timestamp": r.end_ts.strftime("%Y-%d-%mT%H:%M:%S.%f") if r.end_ts else "",
                "num_of_participants": db.session.query(func.count(Vote.vote_id).label('count')).filter(Vote.round_id == r.round_id).one_or_none().count
            }
            for r in rounds
        ], 200

    @staticmethod
    def get_stat(round_id):
        round = Round.query.filter(Round.round_id == round_id).one_or_none()

        if round is None:
            return f"Round not found for ID: {round_id}", 404

        numbers = db.session.query(Vote.number, func.count(Vote.number).label('count')).filter(Vote.round_id == round_id).group_by(Vote.number).order_by('number')

        return [
            {
                "number": n.number,
                "count": n.count
            }
            for n in numbers
        ], 200

    @staticmethod
    def get_active_round_id():
        r = Round.query.filter(Round.end_ts.is_(None)).one_or_none()
        if r is None:
            return None
        else:
            return r.round_id

