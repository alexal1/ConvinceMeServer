import threading

from flask import Flask
from flask_cors import CORS

from logger import logger
from routes import bp

app = Flask(__name__)
lock = threading.Lock()
cors = CORS(app)
app.logger.addHandler(logger)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
