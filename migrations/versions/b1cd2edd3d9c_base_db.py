"""base db

Revision ID: b1cd2edd3d9c
Revises: 
Create Date: 2019-10-22 20:51:07.286837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1cd2edd3d9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('staff',
    sa.Column('staff_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('staff_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_title', sa.String(), nullable=False),
    sa.Column('venue', sa.String(), nullable=False),
    sa.Column('date_start', sa.DateTime(), nullable=True),
    sa.Column('date_end', sa.DateTime(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['staff.staff_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('event_slot',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.PrimaryKeyConstraint('event_id', 'event_date')
    )
    op.create_table('booking',
    sa.Column('booking_no', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('event_date', sa.DateTime(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_date'], ['event_slot.event_date'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('booking_no'),
    sa.UniqueConstraint('event_date'),
    sa.UniqueConstraint('event_id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_table('event_slot')
    op.drop_table('event')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('staff')
    # ### end Alembic commands ###