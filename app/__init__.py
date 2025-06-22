from flask import Flask, jsonify
from .routes import bp
from .metrics import setup_metrics

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    setup_metrics(app)

    @app.route('/')
    def home():
        return jsonify({'status': 'ok'}), 200

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)
