from flask_admin.contrib.sqla import ModelView
from flask_admin import form
from flask_login import current_user, login_required
from wtforms import validators
from flask import url_for, Markup, redirect
import os

from app import bcrypt

class UserView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('flask__admin.login'))
    column_display_pk = True

    can_create = True
    can_edit = False
    can_delete = False
    can_export = False

    form_args = {
        'admin_name': dict(label='Юзер', validators=[validators.DataRequired()]),

        'password': dict(label='Пароль', validators=[validators.DataRequired()])
    }

    column_exclude_list = ['password']

    form_excluded_columns = ['id']

    def create_form(self, obj=None):
        return super(UserView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(UserView, self).edit_form(obj)

    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password)