from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import FarmField, Farm
from app.extensions import db, bcrypt


auth_field_bp = Blueprint('auth_field_bp', __name__)

@auth_field_bp.route('/auth/field')
@login_required
def index():
    if current_user.permission != 1:  
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    children_1 = FarmField.query.join(Farm, FarmField.farm_id == Farm.id) \
                            .filter(Farm.company_id == current_user.company_id) \
                            .all()

    children_2 = Farm.query.filter(Farm.company_id == current_user.company_id, Farm.deleted_at == None).all()
    
    # Create a dictionary to map farm_id to farm.name
    farm_map = {farm.id: farm.name for farm in children_2}
    
    return render_template('auth/field.html', current_user=current_user, children_1=children_1, farm_map=farm_map, children_2=children_2)

@auth_field_bp.route('/auth/add_field_modal', methods=['POST'])
@login_required
def add_field_modal():
    if current_user.permission != 1:
        flash('Unauthorized access')
        return redirect(url_for('main.home'))

    name = request.form['name']
    acreage = request.form['acreage']
    farm_id = request.form['farm_id']

    # Validate inputs
    if not name or not acreage or not farm_id:
        flash('All fields are required.')
        return redirect(url_for('auth_field_bp.index'))

    new_field = FarmField(
        name=name,
        acreage=acreage,
        farm_id=farm_id
    )
    db.session.add(new_field)
    db.session.commit()
    flash('Field successfully added!')
    return redirect(url_for('auth_field_bp.index'))


@auth_field_bp.route('/auth/edit_field/<int:field_id>', methods=['POST'])
@login_required
def edit_field(field_id):
    field = FarmField.query.get_or_404(field_id)
    if current_user.permission != 1:  # O
        flash('Unauthorized access')
        return redirect(url_for('auth_field_bp.index'))

    name = request.form['name']
    acreage = request.form['acreage']
    farm_id = request.form['farm_id']

    # Validate inputs
    if not name or not acreage or not farm_id:
        flash('All fields are required.')
        return redirect(url_for('auth_field_bp.index'))

    field.name = name
    field.acreage = acreage
    field.farm_id = farm_id

    db.session.commit()
    flash('Field successfully updated!')
    return redirect(url_for('auth_field_bp.index'))



@auth_field_bp.route('/auth/delete_field/<int:field_id>')
@login_required
def delete_field(field_id):
    field = FarmField.query.get_or_404(field_id)
    if current_user.permission != 1:  
        flash('Unauthorized access')
        return redirect(url_for('auth_field_bp.index'))  # Update the URL endpoint to 'auth_field_bp.index'

    db.session.delete(field)
    db.session.commit()
    flash('field successfully deleted!')
    return redirect(url_for('auth_field_bp.index'))  # Update the URL endpoint to 'auth_field_bp.index'