"""fresh db

Revision ID: 7866ac2e88f8
Revises: 
Create Date: 2019-10-31 01:32:48.185243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7866ac2e88f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('admin_id', name=op.f('pk_admin'))
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_admin_username'), ['username'], unique=True)

    op.create_table('event_type',
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('type_id', name=op.f('pk_event_type'))
    )
    with op.batch_alter_table('event_type', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_type_name'), ['name'], unique=True)

    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('is_staff', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('venue',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('venue_id', name=op.f('pk_venue'))
    )
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_venue_name'), ['name'], unique=True)

    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('duration', sa.Float(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('img_root', sa.String(), nullable=True),
    sa.Column('is_launched', sa.Boolean(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['event_type.type_id'], name=op.f('fk_event_type_id_event_type')),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.venue_id'], name=op.f('fk_event_venue_id_venue')),
    sa.PrimaryKeyConstraint('event_id', name=op.f('pk_event'))
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_title'), ['title'], unique=False)

    op.create_table('event_slot',
    sa.Column('slot_id', sa.Integer(), nullable=False),
    sa.Column('event_date', sa.DateTime(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], name=op.f('fk_event_slot_event_id_event')),
    sa.PrimaryKeyConstraint('slot_id', name=op.f('pk_event_slot'))
    )
    op.create_table('booking',
    sa.Column('booking_no', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_slot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_slot_id'], ['event_slot.slot_id'], name=op.f('fk_booking_event_slot_id_event_slot')),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name=op.f('fk_booking_user_id_user')),
    sa.PrimaryKeyConstraint('booking_no', name=op.f('pk_booking'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_table('event_slot')
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_title'))

    op.drop_table('event')
    with op.batch_alter_table('venue', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_venue_name'))

    op.drop_table('venue')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    with op.batch_alter_table('event_type', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_type_name'))

    op.drop_table('event_type')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_admin_username'))
        batch_op.drop_index(batch_op.f('ix_admin_email'))

    op.drop_table('admin')
    # ### end Alembic commands ###
