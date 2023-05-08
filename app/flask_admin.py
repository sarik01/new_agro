from flask_login import logout_user, login_user, login_required
from flask import request, jsonify, Blueprint, render_template, redirect, url_for, flash
from .models import AdminFlask
from . import db, login_manager, bcrypt

flask__admin = Blueprint('flask__admin', __name__, template_folder='admin')


def createAdmin2():
    hash_pw = bcrypt.generate_password_hash("123456".encode('utf8'))
    admin = AdminFlask(admin_name='admin', password=hash_pw.decode("utf-8"))

    db.session.add(admin)
    db.session.commit()
    print('admin created!')


@login_manager.user_loader
def load_user(user_id):
    return AdminFlask.query.get(int(user_id))


# @flask__admin.route('/createadmin')
# @login_required
# def createAdmin():
#     hash_pw = bcrypt.generate_password_hash('123456')
#     admin = AdminFlask(admin_name='admin', password=hash_pw)
#
#     db.session.add(admin)
#     db.session.commit()
#     print('admin created!')
#     return jsonify({'msg': 'created!'}, 200)


@flask__admin.route('/login_admin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        admin = AdminFlask.query.filter_by(admin_name=request.form.get('name')).first()
        if admin:
            if bcrypt.check_password_hash(admin.password, request.form.get('pw')):
                login_user(admin)

                print('krasavchik')
                # return jsonify({'msg': 'ok'}, 200)
                # flash('You logged in!', 'green')
                return redirect('/admin')
            else:
                print('chort')
                # return jsonify({'msg': 'incorrect password or username'}, 401)
                flash('incorrect password', 'info')
                return redirect('/admin')
        else:
            flash('incorrect username', 'info')
            return redirect('/admin')
    return redirect('/admin')


@flask__admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out!', 'success')
    return redirect('/admin')
