from sqlalchemy import ForeignKey
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(entry):
	if entry[0] == 'User':
		return User.query.get(int(entry[1]))
	elif entry[0] == 'Staff':
		return Staff.query.get(int(entry[1]))


class User(UserMixin, db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), index=True, unique=True, nullable=False)
	email = db.Column(db.String(255), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(255))

    # This is a replacement for tostring
	def __repr__(self):
		return '<Username: {}>'.format(self.username)

	def get_id(self):
		return ('User', self.user_id)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Staff(UserMixin, db.Model):
	staff_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(255), unique=True)
	password_hash = db.Column(db.String(255))
	events = db.relationship('Event', backref='creator', lazy='dynamic')

	def __repr__(self):
		return '<Username: {}>'.format(self.username)

	def get_id(self):
		return ('Staff', self.staff_id)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String, nullable=False)
    venue = db.Column(db.String, nullable=False)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    capacity = db.Column(db.Integer)
    type = db.Column(db.String)
    description = db.Column(db.String)
    created_by = db.Column(db.Integer, ForeignKey('staff.staff_id'))
    price = db.Column(db.Integer)


    def __repr__(self):
        return "Event ID: {}\n" \
               "Event Title: {}\n" \
               "Organizer: {}".format(self.event_id, self.event_title, self.created_by)


class EventSlot(db.Model):
    event_id = db.Column(db.Integer, ForeignKey('event.event_id'), primary_key=True)
    event_date = db.Column(db.DateTime, primary_key=True)

    def __repr__(self):
        return "ID: {}\nDate:".format(self.event_id, self.event_date)


class Booking(db.Model):
    booking_no = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), unique=True)
    event_id = db.Column(db.Integer, ForeignKey('event.event_id'), unique=True)
    event_date = db.Column(db.DateTime, ForeignKey('event_slot.event_date'), unique=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Booking No: {}\nUserID: {}".format(self.booking_no, self.user_id)
