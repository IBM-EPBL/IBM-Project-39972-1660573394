from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "vhjkjvhjk"

    from .views import blue_print
    app.register_blueprint(blue_print, url_prefix="/")

    return app