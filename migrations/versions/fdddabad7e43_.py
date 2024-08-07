"""empty message

Revision ID: fdddabad7e43
Revises: 
Create Date: 2024-07-03 08:58:28.687722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdddabad7e43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('harvest_per_field', schema=None) as batch_op:
        batch_op.alter_column('yield_type',
               existing_type=sa.FLOAT(),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('harvest_per_field', schema=None) as batch_op:
        batch_op.alter_column('yield_type',
               existing_type=sa.String(length=80),
               type_=sa.FLOAT(),
               existing_nullable=False)

    # ### end Alembic commands ###
