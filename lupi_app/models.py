from datetime import datetime
from lupi_app.config import db


class Round(db.Model):
    __tablename__ = 'round'
    round_id = db.Column(db.Integer, primary_key=True)
    start_ts = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    end_ts = db.Column(db.DateTime)
    winner = db.Column(db.Integer, db.ForeignKey('vote.vote_id'))


class Vote(db.Model):
    __tablename__ = 'vote'
    vote_id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id'), index=True, nullable=False)
    vote_ts = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    name = db.Column(db.String(32), index=True, nullable=False)
    number = db.Column(db.Integer, nullable=False)
