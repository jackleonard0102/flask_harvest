from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect
from app.models import User, Customer, Farm, FarmField, Harvest, HarvestPerField, Truck, HarvestRig, Truckload

class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email', 'permission', 'company_id')
    form_columns = ('username', 'email', 'permission', 'company_id', 'password_hash')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission == 0  # Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class CustomerAdmin(ModelView):
    column_list = ('id', 'name', 'address', 'status')
    form_columns = ('name', 'address', 'status')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class FarmAdmin(ModelView):
    column_list = ('id', 'name', 'email', 'address', 'company_id')
    form_columns = ('name', 'email', 'address', 'company_id')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class FarmFieldAdmin(ModelView):
    column_list = ('id', 'name', 'acreage', 'farm_id')
    form_columns = ('name', 'acreage', 'farm_id')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class HarvestAdmin(ModelView):
    column_list = ('id', 'name', 'date', 'farm_id')
    form_columns = ('name', 'date', 'farm_id')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class HarvestPerFieldAdmin(ModelView):
    column_list = ('id', 'harvest_id', 'field_id', 'yield_amount', 'yield_type')
    form_columns = ('harvest_id', 'field_id', 'yield_amount', 'yield_type')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class TruckAdmin(ModelView):
    column_list = ('id', 'name', 'year', 'vin', 'current_driver_id', 'company_id')
    form_columns = ('name', 'year', 'vin', 'current_driver_id', 'company_id')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class HarvestRigAdmin(ModelView):
    column_list = ('id', 'name', 'year', 'serial_number', 'current_operator_id', 'company_id')
    form_columns = ('name', 'year', 'serial_number', 'current_operator_id', 'company_id')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.permission <= 1  # Admin and Superadmin

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


class TruckloadAdmin(ModelView):
    column_list = ('id', 'load_date_time', 'unload_date_time', 'harvest_rig_id', 'operator_id', 'truck_id', 'trucker_id', 'field_id', 'harvest_id', 'yield_amount', 'yield_type')
    form_columns = ('load_date_time', 'unload_date_time', 'harvest_rig_id', 'operator_id', 'truck_id', 'trucker_id', 'field_id', 'harvest_id', 'yield_amount', 'yield_type')

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.permission <= 1 or current_user.permission == 3)  # Admin, Superadmin, or Office

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


def setup_admin(app, db):
    admin = Admin(app, name='Harvest App', template_mode='bootstrap3', endpoint='admin')
    admin.add_view(UserAdmin(User, db.session, name='UserAdmin'))
    admin.add_view(CustomerAdmin(Customer, db.session, name='CustomerAdmin'))
    admin.add_view(FarmAdmin(Farm, db.session, name='FarmAdmin'))
    admin.add_view(FarmFieldAdmin(FarmField, db.session, name='FarmFieldAdmin'))
    admin.add_view(HarvestAdmin(Harvest, db.session, name='HarvestAdmin'))
    admin.add_view(HarvestPerFieldAdmin(HarvestPerField, db.session, name='HarvestPerFieldAdmin'))
    admin.add_view(TruckAdmin(Truck, db.session, name='TruckAdmin'))
    admin.add_view(HarvestRigAdmin(HarvestRig, db.session, name='HarvestRigAdmin'))
    admin.add_view(TruckloadAdmin(Truckload, db.session, name='TruckloadAdmin'))
