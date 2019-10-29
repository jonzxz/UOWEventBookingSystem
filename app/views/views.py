#from app import db, routes
from app.views.utils import is_staff_user, is_admin_user #, event_view_formatter, check_slot_clash, \
#							img_filename_gen, event_venue_choices, event_type_choices
#from app.models.users import User, Admin
#from app.models.events import Event, EventSlot
from flask import redirect, url_for
#from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
#from wtforms import SelectField
#from flask_admin.form.upload import ImageUploadField
#from wtforms.validators import DataRequired, NumberRange, ValidationError
#from app.forms.custom_validators import Interval, DateInRange
#from sqlalchemy.sql import func
#from datetime import date, timedelta
#from pathlib import Path
#from os import path


class GlobalIndexView(AdminIndexView):
	def is_accessible(self):
		return is_admin_user() or is_staff_user()

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('staff_login'))


class StaffBaseView(ModelView):
	def is_accessible(self):
		return is_staff_user()

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('staff_login'))


class StaffVenueView(StaffBaseView):
	# List View Settings
	column_display_pk = True
	column_labels = dict(venue_id='ID')
	form_columns = [ 'name' ]


'''
class StaffUserView(StaffBaseView):
	# List View Settings
	can_create = False
	can_edit = False
	can_delete = False
	column_display_pk = True
	column_labels = dict(user_id='ID')
	column_exclude_list = ['password_hash']


class StaffEventView(StaffBaseView):
	# File Paths
	par_dir = Path(__file__).parents[1]
	upload_path = path.join(par_dir, 'static/images')

	# List View Settings
	can_view_details = True
	column_display_pk = True
	column_list = [ 'creator', 'is_scheduled', 'event_id', 'title', 'event_type',
					'duration', 'venue', 'capacity', 'price', 'img_root' ]
	column_labels = dict(is_scheduled='Scheduled', event_id='ID', event_type='Type',
						 duration='Duration (H)', img_root='Image File')

	# Details View Settings
	column_details_list = [ 'event_id', 'title', 'slots', 'venue', 'duration',
							'capacity', 'event_type', 'description', 'price',
							'img_root', 'creator' ]

	# Create/Edit Form Settings
	form_extra_fields = {'path':
						 	ImageUploadField('Upload image',
							base_path=upload_path,
							thumbnail_size=(200, 200, True),
							namegen=img_filename_gen)
						}
	form_overrides = dict(event_type=SelectField,
						  venue=SelectField )

	form_columns = [ 'creator', 'title', 'event_type', 'description', 'duration',
					 'venue', 'capacity', 'price', 'img_root', 'path' ]
	form_args = dict(event_type=dict(choices=event_type_choices),
					 duration=dict(validators=[NumberRange(min=0.5),
											   Interval(interval=0.25)]),
					 venue=dict(choices=event_venue_choices),
					 capacity=dict(validators=[NumberRange(min=1)]),
					 price=dict(validators=[NumberRange(min=0.0)]) )
	form_widget_args = { 'img_root' : {'readonly' : True} }

	# Perform data validation when creating/editing an event
	def on_model_change(self, form, model, is_created):
		creator_entry = form.creator.data
		if creator_entry is None:
			raise ValidationError('Event must have a creator.')
		elif is_created:
			if creator_entry != current_user:
				raise ValidationError('Cannot create event for other admin users.')
		elif model.is_scheduled:
			for slot in model.slots:
				new_start = slot.event_date
				new_end = new_start + timedelta(minutes=int(model.duration * 60))
				timing = (new_start, new_end)

				schedule = db.session.query(Event, EventSlot)\
							.join(EventSlot, Event.event_id == EventSlot.event_id)\
							.filter(Event.venue == model.venue)\
							.filter(func.Date(EventSlot.event_date) ==
									func.Date(new_start)).all()

				check_slot_clash(schedule, timing, slot.slot_id)


class StaffEventSlotView(StaffBaseView):
	# List View Settings
	can_view_details = True
	column_display_pk = True
	column_list = [ 'slot_id', 'event', 'event_date', 'start_time', 'end_time' ]

	column_labels = dict(slot_id='ID', event_date='Date',
						 start_time='Start', end_time='End')

	column_sortable_list = ( 'slot_id', ('event', 'event.title'), 'event_date')
	column_type_formatters = event_view_formatter

	# Create/Edit Form Settings
	form_args = dict( event=dict(validators=[DataRequired()]),
					  event_date=dict(validators=[DateInRange()]) )

	# Perform data validation when creating/editing a slot
	def on_model_change(self, form, model, is_created):
		duration = form.event.data.duration
		new_start = model.event_date
		new_end = new_start + timedelta(minutes=duration * 60)
		timing = (new_start, new_end)

		new_venue = form.event.data.venue
		schedule = db.session.query(Event, EventSlot)\
					.join(EventSlot, Event.event_id == EventSlot.event_id)\
					.filter(Event.venue == new_venue).all()

		check_slot_clash(schedule, timing, model.slot_id)


### To Update ###
class StaffBookingView(StaffBaseView):
	column_display_pk = True
'''