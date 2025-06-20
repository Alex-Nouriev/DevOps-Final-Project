from flask import Flask
from .routes import bp
from .metrics import setup_metrics



def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    setup_metrics(app)
    return app



if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)
