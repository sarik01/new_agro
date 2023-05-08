from flask import current_app

from app import create_app, db, redis
from app.flask_admin import createAdmin2
from app.models import User, AdminFlask

app = create_app()



def user_admin():
    u = User(
        username='admin',

    )

    u.save_password('6569321John0604')
    u.save()
    print('UserAdmin created!')


if __name__ == "__main__":

    with app.app_context():
        redis.flushdb()
        db.create_all()

        u = User.query.filter_by(username='admin').first()

        admin = AdminFlask.query.filter_by(admin_name='admin').first()

        if not u:
            user_admin()

        if not admin:
            createAdmin2()

        app.run(debug=True, host="0.0.0.0", port=5001)
