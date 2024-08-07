from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.permission == 0:
            return redirect(url_for('company.index'))
        elif current_user.permission == 1:
            return redirect(url_for('auth_user_bp.index'))
        elif current_user.permission == 2:
            return redirect(url_for('operator_rig_bp.index'))
        elif current_user.permission == 3:
            return redirect(url_for('office_truckloads_bp.index'))
        elif current_user.permission == 4:
            return redirect(url_for('trucker_bp.index'))
        else:
            # You can add more conditions for other permission levels if needed.
            pass
    return redirect(url_for('authentication.login'))