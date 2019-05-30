"""empty message

Revision ID: 50002283698a
Revises: 47eadcc46755
Create Date: 2019-05-28 14:47:17.143824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50002283698a'
down_revision = '47eadcc46755'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image')
    # ### end Alembic commands ###