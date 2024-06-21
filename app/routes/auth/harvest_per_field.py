from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import HarvestPerField, Harvest, FarmField, Farm
from app.extensions import db

auth_harvest_per_field_bp = Blueprint('auth_harvest_per_field_bp', __name__)

@auth_harvest_per_field_bp.route('/auth/harvest_per_field')
@login_required
def index():
    if current_user.permission != 1:  # Suppose 0 and 1 are permissions for superauth and auth
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    children_1 = HarvestPerField.query.all()

    # Correct usage of query and join
    children_2 = db.session.query(Harvest).join(Farm, Harvest.farm_id == Farm.id) \
                        .filter(Farm.company_id == current_user.company_id) \
                        .all()
    children_3 = db.session.query(FarmField).join(Farm, FarmField.farm_id == Farm.id) \
                        .filter(Farm.company_id == current_user.company_id) \
                        .all()
    
    # Create dictionaries to map harvest_id and field_id to their names
    harvest_map = {harvest.id: harvest.name for harvest in children_2}
    field_map = {field.id: field.name for field in children_3}
    
    return render_template('auth/harvest_per_field.html', current_user=current_user, children_1=children_1, harvest_map=harvest_map, field_map=field_map, children_2=children_2, children_3=children_3)


@auth_harvest_per_field_bp.route('/auth/add_harvest_per_field_modal', methods=['POST'])
@login_required
def add_harvest_per_field_modal():
    if current_user.permission != 1:
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    harvest_id = request.form['harvest_id']
    field_id = request.form['field_id']
    yield_amount = request.form['yield_amount']
    yield_type = request.form['yield_type']

    # Validate inputs
    if not harvest_id or not field_id:
        flash('All fields are required.')
        return redirect(url_for('auth_harvest_per_field_bp.index'))

    new_harvest_per_field = HarvestPerField(
        harvest_id=harvest_id,
        field_id=field_id,
        yield_amount=yield_amount,
        yield_type=yield_type
    )
    db.session.add(new_harvest_per_field)
    db.session.commit()
    flash('Harvest Per Field successfully added!')
    return redirect(url_for('auth_harvest_per_field_bp.index'))


@auth_harvest_per_field_bp.route('/auth/edit_harvest_per_field/<int:harvest_per_field_id>', methods=['POST'])
@login_required
def edit_harvest_per_field(harvest_per_field_id):
    harvest_per_field = HarvestPerField.query.get_or_404(harvest_per_field_id)
    if current_user.permission != 1:  # Only superauth or auth can edit harvest per fields
        flash('Unauthorized access')
        return redirect(url_for('auth_harvest_per_field_bp.index'))

    harvest_id = request.form['harvest_id']
    field_id = request.form['field_id']
    yield_amount = request.form['yield_amount']
    yield_type = request.form['yield_type']

    # Validate inputs
    if not harvest_id or not field_id:
        flash('All fields are required.')
        return redirect(url_for('auth_harvest_per_field_bp.index'))

    harvest_per_field.harvest_id = harvest_id
    harvest_per_field.field_id = field_id
    harvest_per_field.yield_amount = yield_amount
    harvest_per_field.yield_type = yield_type

    db.session.commit()
    flash('Harvest Per Field successfully updated!')
    return redirect(url_for('auth_harvest_per_field_bp.index'))

@auth_harvest_per_field_bp.route('/auth/delete_harvest_per_field/<int:harvest_per_field_id>')
@login_required
def delete_harvest_per_field(harvest_per_field_id):
    harvest_per_field = HarvestPerField.query.get_or_404(harvest_per_field_id)
    if current_user.permission != 1:  # Only superauth or auth can delete harvest per fields
        flash('Unauthorized access')
        return redirect(url_for('auth_harvest_per_field_bp.index'))

    db.session.delete(harvest_per_field)
    db.session.commit()
    flash('Harvest Per Field successfully deleted!')
    return redirect(url_for('auth_harvest_per_field_bp.index'))