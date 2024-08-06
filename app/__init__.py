# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()
 
 
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('app.config.Config')

#     db.init_app(app)
#     migrate.init_app(app, db)

#     with app.app_context():
#         from . import routes, models
#         db.create_all()

#     return app

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import stripe

# db = SQLAlchemy()
# migrate = Migrate( db)

# def create_app():
#     app = Flask(__name__, static_folder='static', template_folder='templates')
#     app.config.from_object('config.Config')

#     db.init_app(app)
#     migrate.init_app(app, db)

#     stripe.api_key = app.config['STRIPE_API_KEY']

#     with app.app_context():
#         from . import models, routes
#         db.create_all()

#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from . import models, routes
        db.create_all()

    return app
