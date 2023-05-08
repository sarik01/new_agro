import json
import math
import calendar
from functools import lru_cache, cached_property

from flask import jsonify
from flask_login import UserMixin

from . import db
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash


class JsonEcodeDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '[]'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        else:
            return json.loads(value)


class AdminFlask(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_json(self):
        wewe = self.id
        res = vars(self)
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()


class Users(BaseModel):
    name = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.Text, nullable=True)
    remember_token = db.Column(db.Text, nullable=True)

    # role_metas = relationship("Role_meta", cascade="all,delete", backref="user", lazy=True)

    def save_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'email_verified_at': self.email_verified_at,
            'remember_token': self.remember_token,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Regions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    region_code = db.Column(db.String(), unique=True, nullable=True)

    def to_json(self):
        wewe = self.id
        res = vars(self)
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            # 'created_at': self.created_at,
            # 'updated_at': self.updated_at,
            'name_uz': self.name_uz,
            'name_ru': self.name_ru,
            'region_code': self.region_code,

        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()


class Districts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    region_code = db.Column(db.Integer, nullable=True)
    district_code = db.Column(db.Integer, unique=True, nullable=True)

    def to_json(self):
        wewe = self.id
        res = vars(self)
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        region = db.session.query(Regions.id, Regions.region_code, Regions.name_uz, Regions.name_ru).filter(
            Regions.region_code == self.region_code).first()

        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name_uz': self.name_uz,
            'name_ru': self.name_ru,
            'region': {
                'region_id': region[0] if region else None,
                'region_code': region[1] if region else None,
                'name_uz': region[2] if region else None,
                'name_ru': region[3] if region else None,
            },
            'district_code': self.district_code
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()


class Farms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    region_code = db.Column(db.Integer, nullable=True)
    district_code = db.Column(db.Integer, nullable=True)
    mfy_code = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Text, nullable=True)
    stir = db.Column(db.String(255), nullable=True)
    qfy_name = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    fax = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(255), nullable=True)
    farmer_name = db.Column(db.String(255), nullable=True)
    accountant_name = db.Column(db.String(255), nullable=True)
    agronomist_name = db.Column(db.String(255), nullable=True)
    engineer_name = db.Column(db.String(255), nullable=True)
    mfo = db.Column(db.String(255), nullable=True)
    bank_name = db.Column(db.String(255), nullable=True)
    bar_code = db.Column(db.String(255), nullable=True)
    fields = relationship("Fields", cascade="all,delete", backref="farm_field")

    def to_json(self):
        wewe = self.id
        res = vars(self)
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'stir': self.stir,
            'qfy_name': self.qfy_name,
            'street': self.street,
            'phone': self.phone,
            'fax': self.fax,
            'email': self.email,
            'postal_code': self.postal_code,
            'farmer_name': self.farmer_name,
            'accountant_name': self.accountant_name,
            'agronomist_name': self.agronomist_name,
            'engineer_name': self.engineer_name,
            'mfo': self.mfo,
            'bank_name': self.bank_name,
            'bar_code': self.bar_code,
            'region_code': self.region_code,
            'district_code': self.district_code
        }


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    length = db.Column(db.Float, nullable=True)
    area = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    obstacle_degree = db.Column(db.Float, nullable=True)
    stone_degree = db.Column(db.Integer, nullable=True)
    skewness_degree = db.Column(db.Integer, nullable=True)
    zone = db.Column(db.Integer, nullable=True)
    number = db.Column(db.String(255), nullable=True)
    shape_degree = db.Column(db.Integer, nullable=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'length': self.length,
            'area': self.area,
            'width': self.width,
            'obstacle_degree': self.obstacle_degree,
            'skewness_degree': self.skewness_degree,
            'zone': self.zone,
            'number': self.number,
            'farm_id': self.farm_id
        }


class Machines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    type = db.Column(db.Integer, nullable=True)
    inventor_number = db.Column(db.String(155), nullable=True)
    model = db.Column(db.String(155), nullable=True)
    name = db.Column(db.String(155), nullable=True)
    price = db.Column(db.String(155), nullable=True)
    balance = db.Column(db.Float, nullable=True)
    technical_resource = db.Column(db.Float, nullable=True)
    annual_amortization = db.Column(db.Float, nullable=True)
    annual_repair = db.Column(db.Float, nullable=True)
    annual_service = db.Column(db.Float, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'type': self.type,
            'inventor_number': self.inventor_number,
            'model': self.model,
            'name': self.name,
            'price': self.price,
            'balance': self.balance,
            'technical_resource': self.technical_resource,
            'annual_amortization': self.annual_amortization,
            'annual_repair': self.annual_repair,
            'annual_service': self.annual_service,
        }


from numba import njit, jit


class Mfies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    region_code = db.Column(db.Integer, nullable=True)
    district_code = db.Column(db.Integer, nullable=True)
    mfy_code = db.Column(db.Integer, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        region = db.session.query(Regions.id, Regions.region_code, Regions.name_uz, Regions.name_ru).filter(
            Regions.region_code == self.region_code).first()
        district = db.session.query(Districts.id, Districts.district_code, Districts.name_uz, Districts.name_ru).filter(
            Districts.district_code == self.district_code).first()

        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name_uz': self.name_uz,
            'name_ru': self.name_ru,
            'region': {
                'region_id': region[0] if region else None if region else None,
                'region_code': region[1] if region else None,
                'name_uz': region[2] if region else None,
                'name_ru': region[3] if region else None,
            },
            'district': {
                'district_id': district[0] if district else None,
                'district_code': district[1] if district else None,
                'name_uz': district[2] if district else None,
                'name_ru': district[3] if district else None,
            },
            'mfy_code': self.mfy_code,
        }


class Plant_Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), nullable=True)
    tech_cards = relationship('Tech_Card', cascade="all,delete", backref="tech_card_for_arrangement", lazy=True)
    arrangements = relationship('Arrangement', cascade="all,delete", backref="arrangement_for_plant", lazy=True)
    meta_plant_arrange = relationship('MetaPlantArrange', cascade="all,delete",
                                      backref="meta_plant_arrange_for_plnt_type")

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name_uz': self.name_uz,
            'name_ru': self.name_ru,
            'slug': self.slug,

        }


class Plugs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    working_group = db.Column(db.String(255), nullable=True)
    enterprise_name = db.Column(db.String(255), nullable=True)
    area_length = db.Column(db.Float, nullable=True)
    change_time = db.Column(db.Float, nullable=True)
    type = db.Column(db.Integer, nullable=True)
    skewness_degree = db.Column(db.Float, nullable=True)
    mixing_degree = db.Column(db.Float, nullable=True)
    vibration_resistance_degree = db.Column(db.Float, nullable=True)
    sleeping_degree = db.Column(db.Float, nullable=True)
    model = db.Column(db.String(255), nullable=True)
    processing_depth = db.Column(db.Float, nullable=True)
    hull_width = db.Column(db.Float, nullable=True)
    corpus_count = db.Column(db.Float, nullable=True)
    soil_resistance_degree = db.Column(db.Float, nullable=True)
    resistance_growth_rate = db.Column(db.Float, nullable=True)
    width_usage_degree = db.Column(db.Float, nullable=True)
    unit_movement_method = db.Column(db.Integer, nullable=True)
    kinematic_length = db.Column(db.Float, nullable=True)
    failure_elimination_time = db.Column(db.Integer, nullable=True)
    final_time_preparation = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Float, nullable=True)
    resistance_degree = db.Column(db.Float, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'working_group': self.working_group,
            'enterprise_name': self.enterprise_name,
            'change_time': self.change_time,
            'type': self.type,
            'skewness_degree': self.skewness_degree,
            'mixing_degree': self.mixing_degree,
            'vibration_resistance_degree': self.vibration_resistance_degree,
            'sleeping_degree': self.sleeping_degree,
            'model': self.model,
            'processing_depth': self.processing_depth,
            'hull_width': self.hull_width,
            'corpus_count': self.corpus_count,
            'soil_resistance_degree': self.soil_resistance_degree,
            'resistance_growth_rate': self.resistance_growth_rate,
            'width_usage_degree': self.width_usage_degree,
            'unit_movement_method': self.unit_movement_method,
            'kinematic_length': self.kinematic_length,
            'failure_elimination_time': self.failure_elimination_time,
            'final_time_preparation': self.final_time_preparation,
            'mass': self.mass,
            'resistance_degree': self.resistance_degree,

        }


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name_uz = db.Column(db.String(255), nullable=True)
    name_ru = db.Column(db.String(255), nullable=True)
    hash = db.Column(db.String(255), nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name_ru': self.name_ru,
            'name_ru': self.name_ru,
            'hash': self.hash,

        }


class Tech_Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.String(255), nullable=True)
    tractor_model = db.Column(db.String(255), nullable=True)
    machine_model = db.Column(db.String(255), nullable=True)
    working_measurement_unit = db.Column(db.String(255), nullable=True)
    working_quantity = db.Column(db.Float, nullable=True)
    working_balance = db.Column(db.Float, nullable=True)
    working_balance = db.Column(db.Float, nullable=True)
    worker_working_days = db.Column(db.Float, nullable=True)
    mechanizator_working_type = db.Column(db.String(255), nullable=True)
    worker_working_type = db.Column(db.String(255), nullable=True)
    mechanizator_salary = db.Column(db.Float, nullable=True)
    worker_salary = db.Column(db.Float, nullable=True)
    fuel_consumption_per_unit = db.Column(db.Float, nullable=True)
    fuel_consumption = db.Column(db.Float, nullable=True)
    continuity = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    usage_area = db.Column(db.Float, nullable=True)
    slug = db.Column(db.Float, nullable=True)
    phase = db.Column(db.Integer, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'tractor_model': self.tractor_model,
            'machine_model': self.machine_model,
            'working_measurement_unit': self.working_measurement_unit,
            'working_quantity': self.working_quantity,
            'working_balance': self.working_balance,
            'working_balance': self.working_balance,
            'worker_working_days': self.worker_working_days,
            'mechanizator_working_type': self.mechanizator_working_type,
            'worker_working_type': self.worker_working_type,
            'mechanizator_salary': self.mechanizator_salary,
            'worker_salary': self.worker_salary,
            'fuel_consumption_per_unit': self.fuel_consumption_per_unit,
            'fuel_consumption': self.fuel_consumption,
            'continuity': self.continuity,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'usage_area': self.usage_area,
            'slug': self.slug,
            'phase': self.phase,

        }


class Agregat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.String(), nullable=False)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tractor_inventor_number': self.tractor_inventor_number,
            'machine_inventor_number': self.machine_inventor_number,
            'machine_inventor_number2': self.machine_inventor_number2,
            'machine_inventor_number3': self.machine_inventor_number3,
            'field_length': self.field_length,
            'quality': self.quality,
            'quality1': self.quality1,
            'measurement': self.measurement,
            'proficiency': self.proficiency,
            'service_id': self.service_id,
        }


class Tractor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    fuel_consumption = db.Column(db.String(), nullable=False)
    amortization = db.Column(db.String(), nullable=False)
    repair = db.Column(db.String(), nullable=False)


class Field_Tech_Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.Text, nullable=True)
    tractor_model = db.Column(db.Text, nullable=True)
    machine_model = db.Column(db.Text, nullable=True)
    working_measurement_unit = db.Column(db.String(255), nullable=True)
    working_quantity = db.Column(db.Float, nullable=True)
    mechanizator_working_type = db.Column(db.String(255), nullable=True)
    worker_working_type = db.Column(db.String(255), nullable=True)
    fuel_consumption_per_unit = db.Column(db.Float, nullable=True)
    usage_area = db.Column(db.Float, nullable=True)
    slug = db.Column(db.String(255), nullable=True)
    phase = db.Column(db.Integer, nullable=True)
    row_space = db.Column(db.Integer, nullable=True)
    plat_type_id = db.Column(db.Integer, nullable=True)
    zone_id = db.Column(db.Integer, nullable=True)
    field_id = db.Column(db.Integer, nullable=True)
    continuity = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'name': self.name,
            'tractor_model': self.tractor_model,
            'machine_model': self.machine_model,
            'working_measurement_unit': self.working_measurement_unit,
            'working_quantity': self.working_quantity,
            'mechanizator_working_type': self.mechanizator_working_type,
            'worker_working_type': self.worker_working_type,
            'fuel_consumption_per_unit': self.fuel_consumption_per_unit,
            'usage_area': self.usage_area,
            'slug': self.slug,
            'phase': self.phase,
            'row_space': self.row_space,
            'plat_type_id': self.plat_type_id,
            'zone_id': self.zone_id,
            'field_id': self.field_id,
            'continuity': self.continuity,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    tax_number = db.Column(db.Text, nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    transaction_no = db.Column(db.Text, nullable=True)
    doc_number = db.Column(db.Text, nullable=True)
    doc_date = db.Column(db.DateTime, nullable=True)
    doc_type = db.Column(db.String(255), nullable=True)
    baunit_type_title = db.Column(db.Text, nullable=True)
    rrr_type_title = db.Column(db.Text, nullable=True)
    legal_area = db.Column(db.Text, nullable=True)
    contour_number = db.Column(db.Text, nullable=True)
    gis_area = db.Column(db.Text, nullable=True)
    massive = db.Column(db.Text, nullable=True)
    tuman = db.Column(db.String(), nullable=True)
    viloyat = db.Column(db.String(), nullable=True)
    executor = db.Column(db.String(), nullable=True)
    bonitet = db.Column(db.String(), nullable=True)
    farm_owner = db.Column(db.String(), nullable=True)
    passport = db.Column(db.String(), nullable=True)
    pnfl = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tax_munber': self.tax_munber,
            'full_name': self.full_name,
            'transaction_no': self.transaction_no,
            'doc_number': self.doc_number,
            'doc_date': self.doc_date,
            'doc_type': self.doc_type,
            'baunit_type_title': self.baunit_type_title,
            'rrr_type_title': self.rrr_type_title,
            'legal_area': self.legal_area,
            'contour_number': self.contour_number,
            'gis_area': self.gis_area,
            'massive': self.massive,
            'tuman': self.tuman,
            'viloyat': self.viloyat,
            'executor': self.executor,
            'bonitet': self.bonitet,
            'fermer_hojaligi': self.fermer_hojaligi,
            'fermer_hojaligi_en': self.fermer_hojaligi_en,
            'passport': self.passport,
            'pnfl': self.pnfl,
            'phone': self.phone,
        }


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=True)

    role_meta = relationship("Role_meta", cascade="delete,all", backref="role", lazy=True)

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Role_meta(db.Model):
    __tablename__ = 'role_meta'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def format(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "role_name": self.role.name,
            "user_id": self.user_id
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    last_login = db.Column(db.DateTime)
    email = db.Column(db.String)
    passport_number = db.Column(db.String)
    pnfl = db.Column(db.String)

    verify_code = db.Column(db.String)

    created_time = db.Column(db.DateTime, default=datetime.now)

    role_metas = relationship("Role_meta", cascade="all,delete", backref="user", lazy=True)

    def save_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'username': self.username,
            'phone': self.phone,
            'last_login': self.last_login,
            'created_time': self.created_time,
            # 'attributes': [{
            #     'key': meta.format()['key'],
            #     'value': meta.format()['value'],
            # } for meta in self.metas]
        }


class Tech_Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    model = db.Column(db.String(), nullable=True)
    machine_name = db.Column(db.String(), nullable=True)
    unit = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=True)
    per_shift = db.Column(db.Float, nullable=True)
    machine_shift = db.Column(db.Float, nullable=True)
    employee_shift = db.Column(db.Float, nullable=True)
    employee = db.Column(db.String(), nullable=True)
    machine = db.Column(db.String(), nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant__types.id'))

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'model': self.model,
            'machine': self.machine,
            'unit': self.unit,
            'total': self.total,
            'per_shift': self.per_shift,
            'machine_shift': self.machine_shift,
            'employee_shift': self.employee_shift,

        }


class Arrangement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.Text, nullable=True)
    # phase = db.Column(db.Text, nullable=True)
    number_of_days = db.Column(db.Text, nullable=True)
    index = db.Column(db.Integer, nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant__types.id'))

    arrangement_copies = relationship('Arrangement_copy',
                                      backref="arrangement_copy")

    unit = db.Column(db.String(), nullable=True)
    balance_norm = db.Column(db.String(), nullable=True)
    discharge = db.Column(db.String(), nullable=True)
    discharge_human = db.Column(db.String(), nullable=True)
    gektar_norma = db.Column(db.Float, nullable=True)
    square_procent = db.Column(db.Float, nullable=True)
    row_space = db.Column(db.Float, nullable=True)
    shift_continuity = db.Column(db.Float, nullable=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('phase.id'))
    # mexanizator_razryadi = db.Column(db.String(), nullable=True)
    # ishchining_razryadi = db.Column(db.String(), nullable=True)

    smenalik_koeffitsiyenti = db.Column(db.Float, nullable=True)
    worker = db.Column(db.String(), nullable=True)
    agregat = db.Column(db.String(), nullable=True)
    bir_birlika = db.Column(db.Float, nullable=True)
    spec_formula = db.Column(db.Text, nullable=True)
    rusumi = db.Column(db.String(200), nullable=True)
    asosiy_mashina_soni = db.Column(db.Float, nullable=True)
    kushimcha_mashina_soni = db.Column(db.Float, nullable=True)
    birictirilgan_mexanizator = db.Column(db.Float, nullable=True)
    group_index = db.Column(db.Integer)

    shablons = db.relationship('Shablon_Arrange', back_populates='arrangement')

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):

        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    # def format(self):
    #     plant = db.session.query(Plant_Types.id, Plant_Types.name_ru, Plant_Types.name_uz).filter(
    #         Plant_Types.id == self.plant_id).first()
    #     return {
    #         'id': self.id,
    #         'created_at': self.created_at,
    #         'updated_at': self.updated_at,
    #         'name': self.name,
    #
    #         'index': self.index,
    #         'plant': {
    #             'id': plant[0], 'name_ru': plant[1], 'name_uz': plant[2]
    #         },
    #         'arrangement_metas': [x.format() for x in self.arrangement_metas],
    #         # 'meta_plant_arrange':[x.format() for x in self.meta_plant_arrange],
    #
    #     }

    def format(self):
        return {

            'id': self.id,
            'created_at': self.created_at,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'updated_at': self.updated_at,
            'name': self.name,
            'number_of_days': self.number_of_days,
            'index': self.index,
            'plant_id': self.plant_id,
            'unit': self.unit,
            'balance_norm': self.balance_norm,
            'discharge': self.discharge,
            'discharge_human': self.discharge_human,
            'gektar_norma': self.gektar_norma,
            'square_procent': self.square_procent,
            'row_space': self.row_space,
            'shift_continuity': self.shift_continuity,
            'phase_id': self.phase_id,
            'smenalik_koeffitsiyenti': self.smenalik_koeffitsiyenti,
            'worker': self.worker,
            'agregat': self.agregat,
            'bir_birlika': self.bir_birlika,
            'asosiy_mashina_soni': self.asosiy_mashina_soni,
            'kushimcha_mashina_soni': self.kushimcha_mashina_soni,
            'birictirilgan_mexanizator': self.birictirilgan_mexanizator,
            'group_index': self.group_index,
        }

    def tech_card(self, gis_area, ekin_id, oil_price, tamirlash, amortizaciya, boshka_ishlarida=None):

        # shift_coefficient = 1.0
        #
        # ret_data = []
        # mechanizaror = []
        # human = []

        shift_coefficient = 1

        ar_metas = ArrangementMeta.query.order_by(ArrangementMeta.index).all()

        discharge_machine = Discharge.query.filter_by(name=self.discharge).first()
        discharge_human = Discharge.query.filter_by(name=self.discharge_human).first()

        # print(f"{discharge_human.name}={self.discharge_human}")
        # print(f"={self.discharge}")

        formulas = []
        for i in ar_metas:
            # print(i.value)
            formulas.append(i.value)

        a = self.gektar_norma

        b = self.square_procent / 100 if self.square_procent else None
        # print(a, b)

        if formulas[0]:
            formula = formulas[0].replace("c", gis_area) if gis_area else None
            formula = formula.replace("a", str(a))
            formula = formula.replace("b", str(b))
        # print(formula)
        result = round(eval(formula), 2)  # if self.unit != 'га' else float(varmeta[1][0]) * 100

        if self.unit == 'га':
            result = float(self.square_procent)

        if formulas[1]:
            if discharge_machine == None:
                formula2 = formulas[1].replace('tractor', str(round(float(self.balance_norm), 2)))
                formula2 = formula2.replace('shift_coeficent', str(shift_coefficient))
                workload = eval(formula2)
            else:
                formula2 = round(float(self.balance_norm) * boshka_ishlarida, 1)
                workload = formula2
        if formulas[2]:
            if discharge_machine == None:
                formula3 = formulas[2].replace('overall', str(result))
                formula3 = formula3.replace('day_norma', str(round(float(self.balance_norm), 2)))
                formula3 = formula3.replace('koef', str(shift_coefficient))
                day_of_shift = eval(formula3)
            else:
                # print(workload)
                formula3 = result / round(float(workload), 2)
                day_of_shift = formula3

        if formulas[3]:
            formula3 = formulas[3].replace('day_of_shift', str(float(day_of_shift)))
            formula3 = formula3.replace('number_of_days', str(float(self.number_of_days)))
        jalo = eval(formula3)
        # result = round(eval(formula3)) if self.unit != 'га' else float(varmeta[1][0]) * 100

        if formulas[4]:
            formula4 = formulas[4].replace('shift_time', str(int(self.shift_continuity)))
            # print(shift_time)
            formula4 = formula4.replace('day_of_shift', str((day_of_shift)))
        workhours = eval(formula4)

        work_machine = round(round(day_of_shift, 2) * discharge_machine.machine) if discharge_machine != None else 0
        work_human = round(round(day_of_shift, 2) * discharge_human.hand_power) if discharge_human != None else 0
        jami_f = round(result * (self.bir_birlika * shift_coefficient), 2) if discharge_machine != None else None
        amortizaciya_f = (amortizaciya.energetic + amortizaciya.kxm) * round(workhours,
                                                                             2) / 1000 if self.discharge else 0
        tamirlash_f = (tamirlash.energetic + tamirlash.kxm) * round(workhours, 2) / 1000 if self.discharge else 0
        boshka_f = jami_f * oil_price / 1000 if self.discharge and discharge_machine != None else 0

        gg = {
            'worker': self.worker,
            'agregat': self.agregat,
            'bir_birlika': round(self.bir_birlika, 2),
            'name': self.name,
            'phase': self.phase.name,
            "plant_id": self.plant_id,
            'id': self.id,
            'number_of_days': float(self.number_of_days),
            'gektar_norma': float(self.gektar_norma),
            'square_procent': float(self.square_procent),
            'square_gektar': round(float(self.square_procent / 100) * round(float(gis_area), 2), 2),
            "result": result,
            'balance_norm': round(float(self.balance_norm), 2),
            'smenalik_koeffitsiyenti': self.smenalik_koeffitsiyenti,
            'shift_continuity': self.shift_continuity,
            # 'workload': float(tractor[0]) * shift_coefficient,
            'workload': workload,
            # 'days_of_shift': round(result / (float(tractor[0]) * shift_coefficient), 2),
            'days_of_shift': round(day_of_shift, 2) if self.discharge != '' else 0,
            'days_of_shift_human': round(day_of_shift, 2) if self.discharge_human != '' else 0,
            # 'day_of_shift': round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            'day_of_shift': round(day_of_shift, 2),
            # 'Jalo': round(round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) / int(self.number_of_days)) if tractor[1] else None,
            'Jalo': math.ceil(jalo) if self.discharge else None,
            # 'work_hours': shift_time * round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            'work_hours': round(workhours, 2) if self.discharge else None,
            'discharge': self.discharge,
            'discharge_human': self.discharge_human,
            'start_time': self.start_time.strftime("%Y.%m.%d") if self.start_time else '',
            'end_time': self.end_time.strftime("%Y.%m.%d") if self.end_time else '',
            'unit': self.unit,
            'index': self.index,
            'work_machine': work_machine,
            'work_human': work_human,
            'bir_birlika_hisob': round(self.bir_birlika * shift_coefficient, 2) if discharge_machine != None else None,
            'jami_xaj_miga': jami_f if jami_f else 0,
            'amor_energitic': amortizaciya.energetic,
            'amor_kxm': amortizaciya.kxm,
            'tamir_energitic': tamirlash.energetic,
            'tamir_kxm': tamirlash.kxm,
            'amortizciya': round(amortizaciya_f, 2),
            'tamirlash': round(tamirlash_f, 2),
            'boshka': boshka_f,
            'jami': round(work_machine + work_human + amortizaciya_f + tamirlash_f + boshka_f, 2),
            'copy': False,
            'tractor': math.ceil(jalo) if self.discharge else None,
            'mehanizator': math.ceil(jalo) * self.birictirilgan_mexanizator if self.birictirilgan_mexanizator else None,
            'kxm_asosiysi': math.ceil(jalo) * self.asosiy_mashina_soni if self.asosiy_mashina_soni else None,
            'kxm_kushimchasi': math.ceil(jalo) * self.kushimcha_mashina_soni if self.kushimcha_mashina_soni else None,
            'ishchi': math.ceil(day_of_shift / float(self.number_of_days)) if self.discharge_human else None,
            'rusumi': self.rusumi,
            'assosiy_mashiba_soni': self.asosiy_mashina_soni,
            'kushimcha_mashina_soni': self.kushimcha_mashina_soni,
            'birictirilgan_mexanizator': self.birictirilgan_mexanizator,
            'group_index': self.group_index,

        }

        return gg


class Arrangement_copy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    name = db.Column(db.Text, nullable=True)
    # phase = db.Column(db.Text, nullable=True)
    number_of_days = db.Column(db.Text, nullable=True)
    index = db.Column(db.Integer, nullable=True)
    plant_id = db.Column(db.Integer, nullable=True)

    unit = db.Column(db.String(), nullable=True)
    balance_norm = db.Column(db.String(), nullable=True)
    discharge = db.Column(db.String(), nullable=True)
    discharge_human = db.Column(db.String(), nullable=True)
    gektar_norma = db.Column(db.Float, nullable=True)
    square_procent = db.Column(db.Float, nullable=True)
    row_space = db.Column(db.Float, nullable=True)
    shift_continuity = db.Column(db.Float, nullable=True)
    phase_id = db.Column(db.Integer, nullable=True)
    # mexanizator_razryadi = db.Column(db.String(), nullable=True)
    # ishchining_razryadi = db.Column(db.String(), nullable=True)

    smenalik_koeffitsiyenti = db.Column(db.Float, nullable=True)
    worker = db.Column(db.String(), nullable=True)
    agregat = db.Column(db.String(), nullable=True)
    bir_birlika = db.Column(db.Float, nullable=True)
    spec_formula = db.Column(db.Text, nullable=True)
    cadastor = db.Column(db.Text, nullable=True)
    gis_area = db.Column(db.Text, nullable=True)
    arrangement_id = db.Column(db.Integer, db.ForeignKey('arrangement.id'))
    rusumi = db.Column(db.String(200), nullable=True)
    asosiy_mashina_soni = db.Column(db.Float, nullable=True)
    kushimcha_mashina_soni = db.Column(db.Float, nullable=True)
    birictirilgan_mexanizator = db.Column(db.Float, nullable=True)
    group_index = db.Column(db.Integer)
    region = db.Column(db.String(250))
    contour_number = db.Column(db.String(250))

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):

        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    # def format(self):
    #     plant = db.session.query(Plant_Types.id, Plant_Types.name_ru, Plant_Types.name_uz).filter(
    #         Plant_Types.id == self.plant_id).first()
    #     return {
    #         'id': self.id,
    #         'created_at': self.created_at,
    #         'updated_at': self.updated_at,
    #         'name': self.name,
    #         'cadastor': self.cadastor,
    #
    #         'index': self.index,
    #         'plant': {
    #             'id': plant[0], 'name_ru': plant[1], 'name_uz': plant[2]
    #         },
    #         'arrangement_metas': [x.format() for x in self.arrangement_metas],
    #         # 'meta_plant_arrange':[x.format() for x in self.meta_plant_arrange],
    #
    #     }

    def format(self):
        return {

            'id': self.id,
            'created_at': self.created_at,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'updated_at': self.updated_at,
            'name': self.name,
            'number_of_days': self.number_of_days,
            'index': self.index,
            'plant_id': self.plant_id,
            'unit': self.unit,
            'balance_norm': self.balance_norm,
            'discharge': self.discharge,
            'discharge_human': self.discharge_human,
            'gektar_norma': self.gektar_norma,
            'square_procent': self.square_procent,
            'row_space': self.row_space,
            'shift_continuity': self.shift_continuity,
            'phase_id': self.phase_id,
            'smenalik_koeffitsiyenti': self.smenalik_koeffitsiyenti,
            'worker': self.worker,
            'agregat': self.agregat,
            'bir_birlika': self.bir_birlika,
            'asosiy_mashina_soni': self.asosiy_mashina_soni,
            'kushimcha_mashina_soni': self.kushimcha_mashina_soni,
            'birictirilgan_mexanizator': self.birictirilgan_mexanizator,
            'group_index': self.group_index,
        }

    @lru_cache(maxsize=None)
    def tech_card(self, gis_area, ekin_id, tuzatish, oil_price, tamirlash, amortizaciya, er_haydashdan=None,
                  zanjirli_tractor_bulsa=None, boshka_ishlarida=None, gildirakli_tractor_bulsa=None):
        # shift_coefficient = 1.0
        #
        # ret_data = []
        # mechanizaror = []
        # human = []

        shift_coefficient = 1

        ar_metas = ArrangementMeta.query.order_by(ArrangementMeta.index).all()

        # print(f"{discharge_human.name}={self.discharge_human}")
        # print(f"={self.discharge}")

        discharge_machine = Discharge.query.filter_by(name=self.discharge).first()
        discharge_human = Discharge.query.filter_by(name=self.discharge_human).first()

        formulas = []
        for i in ar_metas:
            # print(i.value)
            formulas.append(i.value)

        a = self.gektar_norma

        b = self.square_procent / 100 if self.square_procent else None
        # print(a, b)

        if formulas[0]:
            formula = formulas[0].replace("c", gis_area) if gis_area else None
            formula = formula.replace("a", str(a))
            formula = formula.replace("b", str(b))
        # print(formula)
        result = round(eval(formula), 2)  # if self.unit != 'га' else float(varmeta[1][0]) * 100

        if self.unit == 'га':
            result = float(self.square_procent)

        if formulas[1]:
            if discharge_machine == None:
                formula2 = formulas[1].replace('tractor', str(round(float(self.balance_norm), 2)))
                formula2 = formula2.replace('shift_coeficent', str(shift_coefficient))
                workload = eval(formula2)
            else:
                formula2 = round(float(self.balance_norm) * 1, 1)
                workload = formula2
        if formulas[2]:
            if discharge_machine == None:
                formula3 = formulas[2].replace('overall', str(result))
                formula3 = formula3.replace('day_norma', str(round(float(self.balance_norm), 2)))
                formula3 = formula3.replace('koef', str(shift_coefficient))
                day_of_shift = eval(formula3)
            else:
                formula3 = result / round(float(workload), 2)
                day_of_shift = formula3

        if formulas[3]:
            formula3 = formulas[3].replace('day_of_shift', str(float(day_of_shift)))
            formula3 = formula3.replace('number_of_days', str(float(self.number_of_days)))
        jalo = eval(formula3)
        # result = round(eval(formula3)) if self.unit != 'га' else float(varmeta[1][0]) * 100

        if formulas[4]:
            formula4 = formulas[4].replace('shift_time', str(int(self.shift_continuity)))
            # print(shift_time)
            formula4 = formula4.replace('day_of_shift', str((day_of_shift)))
        workhours = eval(formula4)

        work_machine = round(round(day_of_shift, 2) * discharge_machine.machine) if discharge_machine != None else 0
        work_human = round(round(day_of_shift, 2) * discharge_human.hand_power) if discharge_human != None else 0
        jami_f =  round(result * (self.bir_birlika * shift_coefficient), 2) if discharge_machine != None else 0
        amortizaciya_f = (amortizaciya.energetic + amortizaciya.kxm) * round(workhours,
                                                                             2) / 1000 if self.discharge else 0
        tamirlash_f = (tamirlash.energetic + tamirlash.kxm) * round(workhours, 2) / 1000 if self.discharge else 0
        boshka_f = jami_f * oil_price / 1000 if self.discharge and discharge_machine != None else 0
        print(self.id)
        # for i in ar_metas:
        #     if i.arrangement_id == self.id:
        #         boshka_f = eval(i.value)

        gg = {
            'worker': self.worker,
            'agregat': self.agregat,
            'bir_birlika': round(self.bir_birlika, 2) if self.bir_birlika else None,
            'name': self.name,
            'phase': self.arrangement_copy.phase.name,
            "plant_id": self.plant_id,
            'id': self.id,
            'number_of_days': float(self.number_of_days),
            'gektar_norma': float(self.gektar_norma),
            'square_procent': float(self.square_procent),
            'square_gektar': round(float(self.square_procent / 100) * round(float(gis_area), 2), 2),
            "result": result,
            'balance_norm': round(float(self.balance_norm), 2),
            'smenalik_koeffitsiyenti': self.smenalik_koeffitsiyenti,
            'shift_continuity': self.shift_continuity,
            # 'workload': float(tractor[0]) * shift_coefficient,
            'workload': workload,
            # 'days_of_shift': round(result / (float(tractor[0]) * shift_coefficient), 2),
            'days_of_shift': round(day_of_shift, 2) if self.discharge != '' else 0,
            'days_of_shift_human': round(day_of_shift, 2) if self.discharge_human != '' else 0,
            # 'day_of_shift': round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            'day_of_shift': round(day_of_shift, 2),
            # 'Jalo': round(round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) / int(self.number_of_days)) if tractor[1] else None,
            'Jalo': math.ceil(jalo) if self.discharge else None,
            # 'work_hours': shift_time * round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            'work_hours': round(workhours, 2) if self.discharge else None,
            'discharge': self.discharge,
            'discharge_human': self.discharge_human,
            'start_time': self.start_time.strftime("%Y.%m.%d") if self.start_time else '',
            'end_time': self.end_time.strftime("%Y.%m.%d") if self.end_time else '',
            'unit': self.unit,
            'index': self.index,
            'work_machine': work_machine,
            'work_human': work_human,
            'bir_birlika_hisob': round(
                self.bir_birlika * zanjirli_tractor_bulsa if zanjirli_tractor_bulsa else shift_coefficient,
                2) if discharge_machine != None else None,
            'jami_xaj_miga': jami_f if jami_f else 0,
            'amor_energitic': amortizaciya.energetic,
            'amor_kxm': amortizaciya.kxm,
            'tamir_energitic': tamirlash.energetic,
            'tamir_kxm': tamirlash.kxm,
            'amortizciya': round(amortizaciya_f, 2),
            'tamirlash': round(tamirlash_f, 2),
            'boshka': boshka_f,
            'jami': round(work_machine + work_human + amortizaciya_f + tamirlash_f + boshka_f, 2),
            'copy': True,
            'tractor': math.ceil(jalo) if self.discharge else None,
            'mehanizator': math.ceil(jalo) * self.birictirilgan_mexanizator if self.birictirilgan_mexanizator else None,
            'kxm_asosiysi': math.ceil(jalo) * self.asosiy_mashina_soni if self.asosiy_mashina_soni else None,
            'kxm_kushimchasi': math.ceil(jalo) * self.kushimcha_mashina_soni if self.kushimcha_mashina_soni else None,
            'ishchi': math.ceil(day_of_shift / float(self.number_of_days)) if self.discharge_human else None,
            'rusumi': self.rusumi,
            'assosiy_mashiba_soni': self.asosiy_mashina_soni,
            'kushimcha_mashina_soni': self.kushimcha_mashina_soni,
            'birictirilgan_mexanizator': self.birictirilgan_mexanizator,
            'group_index': self.group_index,
            'arrangement_id': self.arrangement_id

        }
        return gg

    @lru_cache(maxsize=None)
    def tech_card_exel(self, gis_area, ekin_id, tuzatish, oil_price, tamirlash, amortizaciya, boshka_ishlarida=None):
        # shift_coefficient = 1.0
        #
        # ret_data = []
        # mechanizaror = []
        # human = []

        shift_coefficient = 1

        ar_metas = ArrangementMeta.query.order_by(ArrangementMeta.index).all()

        # print(f"{discharge_human.name}={self.discharge_human}")
        # print(f"={self.discharge}")

        discharge_machine = Discharge.query.filter_by(name=self.discharge).first()
        discharge_human = Discharge.query.filter_by(name=self.discharge_human).first()

        formulas = []
        for i in ar_metas:
            # print(i.value)
            formulas.append(i.value)

        a = self.gektar_norma

        b = self.square_procent / 100 if self.square_procent else None
        # print(a, b)

        if formulas[0]:
            formula = formulas[0].replace("c", gis_area) if gis_area else None
            formula = formula.replace("a", str(a))
            formula = formula.replace("b", str(b))
        # print(formula)
        result = round(eval(formula), 2)  # if self.unit != 'га' else float(varmeta[1][0]) * 100

        if self.unit == 'га':
            result = float(self.square_procent)

        if formulas[1]:
            if discharge_machine == None:
                formula2 = formulas[1].replace('tractor', str(round(float(self.balance_norm), 2)))
                formula2 = formula2.replace('shift_coeficent', str(shift_coefficient))
                workload = eval(formula2)
            else:
                formula2 = round(float(self.balance_norm) * 1, 1)
                workload = formula2
        if formulas[2]:
            if discharge_machine == None:
                formula3 = formulas[2].replace('overall', str(result))
                formula3 = formula3.replace('day_norma', str(round(float(self.balance_norm), 2)))
                formula3 = formula3.replace('koef', str(shift_coefficient))
                day_of_shift = eval(formula3)
            else:
                formula3 = result / round(float(workload), 2)
                day_of_shift = formula3

        if formulas[3]:
            formula3 = formulas[3].replace('day_of_shift', str(float(day_of_shift)))
            formula3 = formula3.replace('number_of_days', str(float(self.number_of_days)))
        jalo = eval(formula3)
        # result = round(eval(formula3)) if self.unit != 'га' else float(varmeta[1][0]) * 100

        if formulas[4]:
            formula4 = formulas[4].replace('shift_time', str(int(self.shift_continuity)))
            # print(shift_time)
            formula4 = formula4.replace('day_of_shift', str((day_of_shift)))
        workhours = eval(formula4)

        work_machine = round(round(day_of_shift, 2) * discharge_machine.machine) if discharge_machine != None else 0
        work_human = round(round(day_of_shift, 2) * discharge_human.hand_power) if discharge_human != None else 0
        jami_f = round(result * (self.bir_birlika * shift_coefficient), 2) if discharge_machine != None else None
        amortizaciya_f = (amortizaciya.energetic + amortizaciya.kxm) * round(workhours,
                                                                             2) / 1000 if self.discharge else 0
        tamirlash_f = (tamirlash.energetic + tamirlash.kxm) * round(workhours, 2) / 1000 if self.discharge else 0
        boshka_f = jami_f * oil_price / 1000 if self.discharge and discharge_machine != None else 0

        # for i in ar_metas:
        #     if i.arrangement_id == self.id:
        #         boshka_f = eval(i.value)

        gg = {
            'c': self.worker,
            'd': self.agregat,
            # 'bir_birlika': round(self.bir_birlika, 2),
            'b': self.name,
            # 'e': self.arrangement_copy.phase.name,
            # "plant_id": self.plant_id,
            # 'id': self.id,
            # 'number_of_days': float(self.number_of_days),
            # 'gektar_norma': float(self.gektar_norma),
            # 'square_procent': float(self.square_procent),
            # 'square_gektar': round(float(self.square_procent / 100) * round(float(gis_area), 2), 2),
            "f": result,
            'g': round(float(self.balance_norm), 2),
            # 'smenalik_koeffitsiyenti': self.smenalik_koeffitsiyenti,
            # 'shift_continuity': self.shift_continuity,
            # # 'workload': float(tractor[0]) * shift_coefficient,
            # 'workload': workload,
            # # 'days_of_shift': round(result / (float(tractor[0]) * shift_coefficient), 2),
            'h': round(day_of_shift, 2) if self.discharge != '' else 0,
            'i': round(day_of_shift, 2) if self.discharge_human != '' else 0,
            # # 'day_of_shift': round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            # 'day_of_shift': round(day_of_shift, 2),
            # # 'Jalo': round(round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) / int(self.number_of_days)) if tractor[1] else None,
            # 'Jalo': math.ceil(jalo) if self.discharge else None,
            # # 'work_hours': shift_time * round((result / (float(tractor[0]) * shift_coefficient)) / shift_coefficient, 2) if tractor[1] else None,
            # 'work_hours': round(workhours, 2) if self.discharge else None,
            'j': self.discharge,
            'k': self.discharge_human,
            # 'start_time': self.start_time.strftime("%d-%m-%Y") if self.start_time else '',
            # 'end_time': self.end_time.strftime("%d-%m-%Y") if self.end_time else '',
            'e': self.unit,
            'a': self.index,
            'l': work_machine,
            'm': work_human,
            'n': round(self.bir_birlika * shift_coefficient, 2) if discharge_machine != None else 0,
            'o': jami_f if jami_f else 0,
            # 'amor_energitic': amortizaciya.energetic,
            # 'amor_kxm': amortizaciya.kxm,
            # 'tamir_energitic': tamirlash.energetic,
            # 'tamir_kxm': tamirlash.kxm,
            'p': round(amortizaciya_f, 2),
            'q': round(tamirlash_f, 2),
            'r': boshka_f,
            's': round(work_machine + work_human + amortizaciya_f + tamirlash_f + boshka_f, 2),
            # 'copy': True,
            # 'tractor': math.ceil(jalo) if self.discharge else None,
            # 'mehanizator': math.ceil(jalo) * self.birictirilgan_mexanizator if self.birictirilgan_mexanizator else None,
            # 'kxm_asosiysi': math.ceil(jalo) * self.asosiy_mashina_soni if self.asosiy_mashina_soni else None,
            # 'kxm_kushimchasi': math.ceil(jalo) * self.kushimcha_mashina_soni if self.kushimcha_mashina_soni else None,
            # 'ishchi': math.ceil(day_of_shift / float(self.number_of_days)) if self.discharge_human else None,
            # 'rusumi': self.rusumi,
            # 'assosiy_mashiba_soni': self.asosiy_mashina_soni,
            # 'kushimcha_mashina_soni': self.kushimcha_mashina_soni,
            # 'birictirilgan_mexanizator': self.birictirilgan_mexanizator,
            # 'group_index': self.group_index,
            # 'arrangement_id': self.arrangement_id

        }
        return gg


class Phase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    arrangements = relationship('Arrangement', cascade="all,delete", backref="phase")

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }


class ArrangementMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    key = db.Column(db.String(), nullable=True)
    value = db.Column(db.String(), nullable=True)
    index = db.Column(db.Integer, nullable=True)

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'key': self.key,
            'value': self.value,
            'index': self.index,
            'arrangement_id': self.arrangement_id,

        }


class MetaPlantArrange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_type_id = db.Column(db.Integer, db.ForeignKey('plant__types.id'))

    tractor_id = db.Column(db.Integer, db.ForeignKey('tractor.id'))
    agregat_id = db.Column(db.Integer, db.ForeignKey('agregat.id'))
    discharge_id = db.Column(db.Integer, db.ForeignKey('discharge.id'))
    index = db.Column(db.Integer, autoincrement=True)
    varmeta = relationship('VarMeta', cascade="all,delete",
                           backref="meta_plant_arrange_for_arrangement")


class VarMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Float, nullable=True)
    value = db.Column(db.Float, nullable=True)
    metaplantarrange_id = db.Column(db.Integer, db.ForeignKey('meta_plant_arrange.id'))


class Discharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    hand_power = db.Column(db.Float, nullable=False)
    machine = db.Column(db.Float, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'hand_power': self.hand_power,
            'machine': self.machine
        }


class Tuzatish_coef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mehaniz_ish_boshka_ishlarda = db.Column(db.Float, nullable=True)
    mehaniz_ish_er_xaydashda = db.Column(db.Float, nullable=True)
    gildirakli_tractor_bulsa = db.Column(db.Float, nullable=True)
    zanjirli_tractor_bulsa = db.Column(db.Float, nullable=True)
    kul_kuchida_ish = db.Column(db.Integer, nullable=True)
    cadastor_num = db.Column(db.Text, nullable=True)

    def format(self, oil_price=None):
        return {
            'id': self.id,
            'mehaniz_ish': self.mehaniz_ish_boshka_ishlarda,
            'oil_price': oil_price,
            'kul_kuchida_ish': self.kul_kuchida_ish
        }


class Oil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'price': self.price
        }


class Amortizatiya_uchun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    energetic = db.Column(db.Integer, nullable=False)
    kxm = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'energetic': self.energetic,
            'kxm': self.kxm
        }


class Tamirlash_uchun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    energetic = db.Column(db.Integer, nullable=False)
    kxm = db.Column(db.Integer, nullable=False)

    def format(self):
        return {
            'id': self.id,
            'energetic': self.energetic,
            'kxm': self.kxm
        }


class EarthPasport(db.Model):
    __tablename__ = 'earth_passports'
    id = db.Column(db.Integer, primary_key=True)
    one_jadval = db.Column(db.Integer, db.ForeignKey('jadval_one.id'))
    two_jadval = db.Column(db.Integer, db.ForeignKey('jadval_two.id'))
    three_jadval = db.Column(db.Integer, db.ForeignKey('jadval_three.id'))
    four_jadval = db.Column(db.Integer, db.ForeignKey('jadval_four.id'))
    # one_jadval = relationship('JadvalOne', cascade="all,delete", backref="jadvalone")
    # two_jadval = relationship('JadvalTwo', cascade="all,delete", backref="jadvaltwo")
    # three_jadval = relationship('JadvalThree', cascade="all,delete", backref="jadvalthree")
    # four_jadval = relationship('JadvalFour', cascade="all,delete", backref="jadvalfour")
    cadastor_num = db.Column(db.Text)
    gis_area = db.Column(db.String(200))
    counter_number = db.Column(db.String(200))
    bir = db.Column(db.Integer)
    asosi = db.Column(db.Integer)
    ayrisimon = db.Column(db.Integer)
    turt = db.Column(db.Integer)

    suv_taminoti = db.Column(db.String(50))
    shorlanganligi = db.Column(db.String(50))
    ekish_sharoiti = db.Column(db.String(50))
    mintaqa = db.Column(db.String(50))

    tuproq_id = db.Column(db.Integer, db.ForeignKey('tuproq.id'))

    yosh_yoki_kichik = db.Column(db.String(50))
    yirik_daraht = db.Column(db.String(50))

    def format(self):
        return {
            'id': self.id,
            'cadastor_num': self.cadastor_num,
            'tusiclar_ulushi': self.tusiclar_ulushi,
            'gildirakli_va_zanjirli': self.gildirakli_va_zanjirli,
            'gildirakli': self.gildirakli,
            'zanjirli': self.zanjirli,
            'kp1': self.kp1,
            'kp2': self.kp2,
            't1': self.t1,
            't2': self.t2,
            'toshlok_darasi': self.toshlok_darasi,
            'toshlok_darasi_yani': self.toshlok_darasi_yani,
            'ish_umum': self.ish_umum,
            'yonilgi_safirga': self.yonilgi_safirga,
            'dala_guruhi': self.dala_guruhi,
            'er_haydashdan': self.er_haydashdan,
            'er_haydashdan_boshka': self.er_haydashdan_boshka,
        }


class Tuproq(BaseModel):
    tuprokning_name = db.Column(db.String(50))
    tuprokning_kh = db.Column(db.String(50))
    land_passports = relationship('EarthPasport', cascade="all,delete", backref="tuproq_passport")


class Arr_for_set_time(BaseModel):
    __tablename__ = 'arr_for_set_time'
    name = db.Column(db.String(500))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    district_code = db.Column(db.Integer)
    index = db.Column(db.Integer)
    plant_id = db.Column(db.Integer)
    phase_id = db.Column(db.Integer)
    continuity = db.Column(db.Float)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time.strftime("%Y.%m.%d") if self.start_time else '',
            'end_time': self.end_time.strftime("%Y.%m.%d") if self.end_time else '',
            'district_code': self.district_code,
            'index': self.index,
            'plant_id': self.plant_id,
            'continuity': self.continuity,
        }


class Folder(BaseModel):
    __searchable__ = ['cad_number']
    cad_number = db.Column(db.String(200))
    tech_cards = relationship('SavedTechCard', cascade="all,delete", backref="tech_card_folder")

    def folder_list(self):
        return {
            'id': self.id,
            'cad_number': self.cad_number,
        }

    def format(self):
        return {
            'id': self.id,
            'cad_number': self.cad_number,
            # 'tech_cards': [i.format() for i in self.tech_cards]
            'tech_cards': [i.to_json() for i in self.tech_cards]
        }


class SavedTechCard(BaseModel):
    __tablename__ = 'saved_tech_card'

    cad_number = db.Column(db.String(200))
    plant_id = db.Column(db.Integer)
    gis_area = db.Column(db.String(200))
    contour_number = db.Column(db.String(200))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))

    def format(self):
        plant = db.session.query(Plant_Types.name_uz).filter(Plant_Types.id == self.plant_id).first()[0]
        return {
            'id': self.id,
            'cad_number': self.cad_number,
            'plant': plant if plant else self.plant_id,
            'plant_id': self.plant_id,
            'gis_area': self.gis_area,
            'contour_number': self.contour_number,
            'folder_id': self.folder_id,

        }

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res


class Plan(BaseModel):
    geometry = db.Column(JsonEcodeDict)
    globalid = db.Column(db.Text)
    region = db.Column(db.String(200))
    district = db.Column(db.String(200))
    crop_name = db.Column(db.String(200))
    crop_area = db.Column(db.Float)
    kontur_raqami = db.Column(db.Integer)
    massiv = db.Column(db.Text)
    shape_length = db.Column(db.Float)
    shape_area = db.Column(db.Float)

    def format(self):
        cropName = db.session.query(CropName.plant_name, CropName.color_code).filter(
            CropName.er_id == self.crop_name).first()
        return {
            'type': 'Feature',
            'id': self.id,
            'geometry': self.geometry,
            'properties': {
                'globalid': self.globalid,
                'region': self.region,
                'district': self.district,
                'crop_name': cropName[0] if cropName else self.crop_name,
                'crop_code': self.crop_name,
                'crop_area': self.crop_area,
                'kontur_raqami': self.kontur_raqami,
                'massiv': self.massiv,
                'shape_length': self.shape_length,
                'shape_area': self.shape_area,
                'color_code': cropName[1] if cropName else None,
            }

        }

    def crops(self):
        cropName = db.session.query(CropName.plant_name, CropName.color_code).filter(
            CropName.er_id == self.crop_name).first()
        return {
            'id': self.id,
            'crop_name': cropName[0] if cropName else self.crop_name,
            'crop_code': self.crop_name,
        }

class CropName(BaseModel):
    __tablename__ = 'crop_name'

    er_id = db.Column(db.Integer, unique=True)
    plant_name = db.Column(db.String(100))
    color_code = db.Column(db.String(100))


class SavedArrTime(BaseModel):
    plant_id = db.Column(db.Integer)
    cadastor_number = db.Column(db.Text)
    gis_area = db.Column(db.Text)
    contour_number = db.Column(db.String(50))
    first_phase_name = db.Column(db.String(100))
    district_code = db.Column(db.String(50))
    first_phase_start_time = db.Column(db.DateTime, nullable=True)
    first_phase_end_time = db.Column(db.DateTime, nullable=True)
    other_phase_start_time = db.Column(db.DateTime, nullable=True)
    other_phase_end_time = db.Column(db.DateTime, nullable=True)

    def format(self):
        try:
            plant_name = db.session.query(Plant_Types.name_uz).filter(Plant_Types.id == self.plant_id).first()
            d = self.first_phase_end_time - self.first_phase_start_time if self.first_phase_start_time and self.first_phase_end_time else None,
            d2 = self.other_phase_end_time - self.other_phase_start_time if self.other_phase_end_time and self.other_phase_start_time else None,

            months_other_phase = {
                '01': [],
                '02': [],
                '03': [],
                '04': [],
                '05': [],
                '06': [],
                '07': [],
                '08': [],
                '09': [],
                '10': [],
                '11': [],
                '12': [],
            }

            months_first_phase = {
                '01': [],
                '02': [],
                '03': [],
                '04': [],
                '05': [],
                '06': [],
                '07': [],
                '08': [],
                '09': [],
                '10': [],
                '11': [],
                '12': [],
            }

            months_len_first = {
                '01': 0,
                '02': 0,
                '03': 0,
                '04': 0,
                '05': 0,
                '06': 0,
                '07': 0,
                '08': 0,
                '09': 0,
                '10': 0,
                '11': 0,
                '12': 0,
            }

            months_len_other = {
                '01': 0,
                '02': 0,
                '03': 0,
                '04': 0,
                '05': 0,
                '06': 0,
                '07': 0,
                '08': 0,
                '09': 0,
                '10': 0,
                '11': 0,
                '12': 0,
            }

            for i in range(1, d[0].days):
                delta = timedelta(days=i)
                day = self.first_phase_end_time - delta

                converted_date = day.strftime("%Y-%m-%d")

                months_first_phase[day.strftime('%m')].append(converted_date)

            for i in range(1, d2[0].days):
                delta = timedelta(days=i)
                day = self.other_phase_end_time - delta

                converted_date = day.strftime("%Y-%m-%d")

                months_other_phase[day.strftime('%m')].append(converted_date)

            for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                a = len(months_first_phase[i])
                months_len_first[i] = a

            for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
                a = len(months_other_phase[i])
                months_len_other[i] = a
            months_len_other_2 = [{}]
            months_len_first_2 = [{}]
            empty = [{}]
            calendar_obj = {
                'months_len_other': [],
                'months_len_first': [],
                'empty': []

            }

            for k in months_len_first:
                if months_len_first[k] != 0:
                    dict_new = calendar_obj['months_len_first'].append({
                        'days': months_len_first[k],
                        'month': k,
                        'name': self.first_phase_name,
                        'start_time': months_first_phase[k][-1],
                        'end_time': months_first_phase[k][0]
                    })
                    dicti = months_len_first_2[0][k] = months_len_first[k]

            for k in months_len_other:
                if months_len_other[k] != 0:
                    dict_new = calendar_obj['months_len_other'].append({
                        'days': months_len_other[k],
                        'month': k,
                        'name': plant_name[0] if plant_name else self.plant_id,
                        'start_time': months_other_phase[k][-1],
                        'end_time': months_other_phase[k][0]
                    })
                    dicti = months_len_other_2[0][k] = months_len_other[k]

            for k in months_len_other:
                if k not in empty[0] and k not in months_len_first_2[0] and k not in \
                        months_len_other_2[0]:
                    dict_new = calendar_obj['empty'].append(
                        {'days': months_len_other[k], 'month': k, 'name': 'bosh er'})
                    dicti = empty[0][k] = months_len_other[k]

            for k in months_len_first:
                if k not in empty[0] and k not in months_len_first_2[0] and k not in \
                        months_len_other_2[0]:
                    dict_new = calendar_obj['empty'].append(
                        {'days': months_len_first[k], 'month': k, 'name': 'bosh er', })
                    dicti = empty[0][k] = months_len_first[k]

            list_super = []

            for i in calendar_obj['empty']:
                list_super.append(i)

            for i in calendar_obj['months_len_first']:
                list_super.append(i)

            for i in calendar_obj['months_len_other']:
                list_super.append(i)

            # print(list_super)

            return {
                "cadastor_number": self.cadastor_number,
                "contour_number": self.contour_number,
                "district_code": self.district_code,
                "first_phase_end_time": self.first_phase_end_time.strftime(
                    "%Y-%m-%d") if self.first_phase_end_time else None,
                "first_phase_name": self.first_phase_name,
                "first_phase_start_time": self.first_phase_start_time.strftime(
                    "%Y-%m-%d") if self.first_phase_start_time else None,
                "gis_area": self.gis_area,
                'left_day_one': d[0].days if self.first_phase_start_time and self.first_phase_end_time else None,
                'left_day_two': d2[0].days if self.other_phase_end_time and self.other_phase_start_time else None,
                "id": self.id,
                "other_phase_end_time": self.other_phase_end_time.strftime(
                    "%Y-%m-%d") if self.other_phase_end_time else None,
                "other_phase_start_time": self.other_phase_start_time.strftime(
                    "%Y-%m-%d") if self.other_phase_start_time else None,
                "plant_name": plant_name[0] if plant_name else self.plant_id,
                # "months_len_other": months_len_other,
                # "months_len_first": months_len_first,
                'calendar': list_super

            }
        except Exception as e:
            print(e)
            return jsonify({'msg': 'no dates'})

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res


class JadvalOne(BaseModel):
    tusiclar_egalagan = db.Column(db.String(50))
    gildir_va_zanjir = db.Column(db.Float)
    gildir = db.Column(db.Float)
    zanjir = db.Column(db.Float)
    passports = relationship('EarthPasport', cascade="all,delete", backref="jadvalone")

    def format(self):
        return {
            'tusiclar_egalagan': self.tusiclar_egalagan,
            'gildir_va_zanjir': self.gildir_va_zanjir,
            'gildir': self.gildir,
            'zanjir': self.zanjir,
        }


class JadvalTwo(BaseModel):
    kiyaligi = db.Column(db.String(100))
    ishlar_zanjir_kp1 = db.Column(db.Float)
    ishlar_zanjir_kp2 = db.Column(db.Float)
    ishlar_gildir_kp1 = db.Column(db.Float)
    ishlar_gildir_kp2 = db.Column(db.Float)
    boskaish_gildir_kp1 = db.Column(db.Float)
    boskaish_gildir_kp2 = db.Column(db.Float)
    boshkaish_zanjir_kp1 = db.Column(db.Float)
    boshkaish_zanjir_kp2 = db.Column(db.Float)
    passports = relationship('EarthPasport', cascade="all,delete", backref="jadvaltwo")

    def format(self):
        return {
            'kiyaligi': self.kiyaligi,
            'ishlar_zanjir_kp1': self.ishlar_zanjir_kp1,
            'ishlar_zanjir_kp2': self.ishlar_zanjir_kp2,
            'ishlar_gildir_kp1': self.ishlar_gildir_kp1,
            'ishlar_gildir_kp2': self.ishlar_gildir_kp2,
            'boskaish_gildir_kp1': self.boskaish_gildir_kp1,
            'boskaish_gildir_kp2': self.boskaish_gildir_kp2,
            'boshkaish_zanjir_kp1': self.boshkaish_zanjir_kp1,
            'boshkaish_zanjir_kp2': self.boshkaish_zanjir_kp2,
        }


class JadvalThree(BaseModel):
    toshlok_darja = db.Column(db.String(100))
    ish_umum = db.Column(db.Float)
    enligi = db.Column(db.Float)
    passports = relationship('EarthPasport', cascade="all,delete", backref="jadvalthree")

    def format(self):
        return {
            'toshlok_darja': self.toshlok_darja,
            'ish_umum': self.ish_umum,
            'enligi': self.enligi,
        }


class JadvalFour(BaseModel):
    guruh = db.Column(db.String(5))
    length = db.Column(db.String(50))
    er_hayd = db.Column(db.Float)
    boshka_ish = db.Column(db.Float)
    passports = relationship('EarthPasport', cascade="all,delete", backref="jadvalfour")

    def format(self):
        return {
            'guruh': self.guruh,
            'length': self.length,
            'er_hayd': self.er_hayd,
            'boshka_ish': self.boshka_ish,
        }


class Extara_Arrangements(BaseModel):
    name_uz = db.Column(db.Text)
    name_ru = db.Column(db.Text)
    number = db.Column(db.String())

    def to_json(self):
        res = {k: v for k, v in vars(self).items() if not k.startswith("_sa")}
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.to_json()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self.to_json()

    def format(self):
        return {
            'id': self.id,
            'name_uz': self.name_uz,
            'name_ru': self.name_ru,
            'number': self.number,

        }


class Shablon(BaseModel):
    __tablename__ = 'shablon'
    ximicat = db.Column(db.Boolean)
    qator_oraliqi = db.Column(db.Integer)
    nasos = db.Column(db.Integer)
    terim = db.Column(db.Integer)
    mintaqa = db.Column(db.Integer)
    qoshqator = db.Column(db.Integer, default=0)
    ekish_sharoiti = db.Column(db.Integer, default=1)


    arrangements = db.relationship('Shablon_Arrange', back_populates='shablon')

    def format(self):
        return {
            'id': self.id,
            'ximicat': self.ximicat,
            'qator_oraliqi': self.qator_oraliqi,
            'nasos': self.nasos,
            'terim': self.terim,
            'mintaqa': self.mintaqa,
            'qoshqator': self.qoshqator,
            'ekish_sharoiti': self.ekish_sharoiti,
        }


class Shablon_Arrange(BaseModel):
    shablon_id = db.Column('shablon_id', db.Integer, db.ForeignKey('shablon.id'))
    arrangement_id = db.Column('arrangement_id', db.Integer, db.ForeignKey('arrangement.id'))

    arrangement = db.relationship('Arrangement', back_populates='shablons')
    shablon = db.relationship('Shablon', back_populates='arrangements')

    def format(self):
        return {
            'id': self.id,
            'shablon_params_id': self.shablon_id,
            'arrangement_id': self.arrangement_id
        }
