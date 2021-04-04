from flask import Flask
from playground import pg
app = Flask(__name__)
app.register_blueprint(pg)


if __name__ == '__main__':
    app.run()