
from flask import *
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis


login_manager = LoginManager()
login_manager.login_view = 'flask__admin.login'
login_manager.login_message = 'Пожалуйста сначало зарегистрируйтесь!'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
search = Search()
redis = FlaskRedis()

# crontab = Crontab()


from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('flask__admin.login'))


    can_create = True
    can_edit = True
    can_delete = True
    can_export = False


class MyExitView(BaseView):
    @expose('/')

    def exit(self):
        print('s')
        return redirect(url_for('flask__admin.logout'), 302)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    search.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db, render_as_butch=True)
    redis.init_app(app)

    # crontab.init_app(app)

    app.config.update(CELERY_CONFIG={
        'broker_url': 'redis://localhost:6379',
        'result_backend': 'redis://localhost:6379',
    })

    # celery = make_celery(app)


    from .routes import new_agro
    from .flask_admin import flask__admin
    from .models import User, AdminFlask, Farmer, Role
    from .views.user_view import UserView
    app.register_blueprint(new_agro)
    app.register_blueprint(flask__admin)

    admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(UserView(AdminFlask, db.session))

    admin.add_view(AdminModelView(Farmer, db.session))
    admin.add_view(AdminModelView(Role, db.session))

    admin.add_view(MyExitView(name='LogOut', url='exit'))

    @app.route("/", methods=['GET'])
    def home():
        return jsonify({"msg": "Hello World"})

    @app.after_request
    def after_request(response):
        header = response.headers
        header.add('Access-Control-Allow-Origin', '*')
        header.add('Access-Control-Allow-Headers', '*')
        header.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app #celery

