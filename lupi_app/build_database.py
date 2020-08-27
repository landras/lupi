import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from lupi_app.config import db
from lupi_app import config

from lupi_app.models import Round, Vote


def build():
    # Delete database file if it exists currently
    if os.path.exists(config.app.config['SQLITE_FILE']):
        os.remove(config.app.config['SQLITE_FILE'])

    # Create the database
    db.create_all()


if __name__ == "__main__":
    build()
