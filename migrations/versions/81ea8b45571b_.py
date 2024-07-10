"""empty message

Revision ID: 81ea8b45571b
Revises: 88f92332ed7a
Create Date: 2024-07-10 05:39:44.844605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ea8b45571b'
down_revision = '88f92332ed7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=255),
               existing_nullable=False)

    with op.batch_alter_table('truckload', schema=None) as batch_op:
        batch_op.add_column(sa.Column('trucker_confirmation', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('truckload', schema=None) as batch_op:
        batch_op.drop_column('trucker_confirmation')

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=255),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
