from flask import Flask

from logger import logger
from routes import bp

app = Flask(__name__)
app.logger.addHandler(logger)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
