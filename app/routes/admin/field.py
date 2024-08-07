from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import FarmField, Farm, Customer
from app.extensions import db, bcrypt


admin_field_bp = Blueprint('admin_field_bp', __name__)

@admin_field_bp.route('/admin/field')
@login_required
def index():
    if current_user.permission != 0:  # Suppose 0 and 1 are permissions for superadmin and admin
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    active_customer_ids = [customer.id for customer in Customer.query.filter(Customer.deleted_at == None, Customer.status == 'active').all()]
    children_2 = Farm.query.join(Customer, Customer.status == "active").filter(Farm.deleted_at == None, Farm.company_id.in_(active_customer_ids)).all()
    active_farm_ids = [farm.id for farm in children_2]
    children_1 = FarmField.query.filter(FarmField.farm_id.in_(active_farm_ids)).all()
    
    farm_map = {farm.id: farm.name for farm in children_2}
    
    return render_template('admin/field.html', current_user=current_user, children_1=children_1, farm_map=farm_map, children_2=children_2)

@admin_field_bp.route('/add_field_modal', methods=['POST'])
@login_required
def add_field_modal():
    if current_user.permission != 0:
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    name = request.form['name']
    acreage = request.form['acreage']
    farm_id = request.form['farm_id']

    # Validate inputs
    if not name or not acreage or not farm_id:
        flash('All fields are required.')
        return redirect(url_for('admin_field_bp.index'))

    new_field = FarmField(
        name=name,
        acreage=acreage,
        farm_id=farm_id
    )
    db.session.add(new_field)
    db.session.commit()
    flash('Field successfully added!')
    return redirect(url_for('admin_field_bp.index'))


@admin_field_bp.route('/edit_field/<int:field_id>', methods=['POST'])
@login_required
def edit_field(field_id):
    field = FarmField.query.get_or_404(field_id)
    if current_user.permission != 0:
        flash('Unauthorized access')
        return redirect(url_for('admin_field_bp.index'))

    name = request.form['name']
    acreage = request.form['acreage']
    farm_id = request.form['farm_id']

    # Validate inputs
    if not name or not acreage or not farm_id:
        flash('All fields are required.')
        return redirect(url_for('admin_field_bp.index'))

    field.name = name
    field.acreage = acreage
    field.farm_id = farm_id

    db.session.commit()
    flash('Field successfully updated!')
    return redirect(url_for('admin_field_bp.index'))



@admin_field_bp.route('/delete_field/<int:field_id>')
@login_required
def delete_field(field_id):
    field = FarmField.query.get_or_404(field_id)
    if current_user.permission != 0:  # Only superadmin or admin can delete fields
        flash('Unauthorized access')
        return redirect(url_for('admin_field_bp.index'))  # Update the URL endpoint to 'admin_field_bp.index'

    db.session.delete(field)
    db.session.commit()
    flash('field successfully deleted!')
    return redirect(url_for('admin_field_bp.index'))  # Update the URL endpoint to 'admin_field_bp.index'