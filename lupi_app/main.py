import os
import sys
import logging

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from flask import render_template
from lupi_app import config

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s"
                    )

connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api('swagger.yml')


# Create a URL route in our application for "/"
@connex_app.route('/')
def ui():
    return render_template('ui.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    connex_app.run(host=config.app.config['HOST'], port=config.app.config['PORT'], debug=True)
