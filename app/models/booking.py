from app import db
from sqlalchemy import ForeignKey


class Booking(db.Model):
	booking_no = db.Column(db.Integer, primary_key=True)
	quantity = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
	event_slot_id = db.Column(db.Integer, ForeignKey('event_slot.slot_id'))
	### payment_id (to be included later)

	user = db.relationship('User', back_populates='bookings')
	slot = db.relationship('EventSlot', back_populates='bookings')

	def __repr__(self):
		return "Booking No: {}\nUserID: {}".format(self.booking_no, self.user_id)