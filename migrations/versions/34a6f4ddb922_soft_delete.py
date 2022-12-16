"""soft delete

Revision ID: 34a6f4ddb922
Revises: 55e0753f057d
Create Date: 2022-12-16 23:47:50.509780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34a6f4ddb922'
down_revision = '55e0753f057d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note_model', sa.Column('deleted', sa.Boolean(), server_default=sa.text('0'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('note_model', 'deleted')
    # ### end Alembic commands ###