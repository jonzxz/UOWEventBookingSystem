from app.models.users import User, Admin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
					SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError, \
								NumberRange, Email
#from wtforms_components import NumberInput
from datetime import date


def RaiseError(field, message='Invalid data'):
	error_list = list(field.errors)
	error_list.append(message)
	field.errors = tuple(error_list)


class BaseLogin(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class MemberLoginForm(BaseLogin):
	def validate(self):
		user = User.query.filter(User.is_staff == False,
								 User.username == self.username.data).first()

		if user is None:
			RaiseError(self.username, message='Invalid username')
			return False
		if not user.check_password(self.password.data):
			RaiseError(self.password, message='Incorrect password')
			return False
		return True


class StaffLoginForm(BaseLogin):
	def validate(self):
		self.usergroup = 'staff'
		target_name = self.username.data
		user = User.query.filter(User.is_staff, User.username == target_name).first()

		if user is None:
			self.usergroup = 'admin'
			user = Admin.query.filter(Admin.username == target_name).first()

		if user is None:
			RaiseError(self.username, message='Invalid username')
			return False
		if not user.check_password(self.password.data):
			RaiseError(self.password, message='Incorrect password')
			return False
		return True



class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(),
					EqualTo('password', message='Password must match!')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already taken')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email already taken')


class SearchForm(FlaskForm):
	CHOICES = [('title', 'Title'),
			   ('date', 'Date'),
			   ('type', 'Type' ),
			   ('price', 'Price')]
	RANGES = [('free', 'FREE'),
			  ('cheap', '< $20'),
			  ('mid', '$20 - 50'),
			  ('expensive', '> $50')]
	STRING_FIELD = StringField()
	DATE_FIELD = DateField(default=date.today())
	PRICE_FIELD = SelectField(choices=RANGES)

	search_field = STRING_FIELD
	search_type = SelectField(choices=CHOICES)
	submit_search = SubmitField('Search')


'''
class BookingForm(FlaskForm):
	title = StringField(render_kw={'readonly':'True'})
	username = StringField(render_kw={'readonly':'True'})
	date = SelectField()
	count = IntegerField('Count', default=1, validators=[DataRequired(), NumberRange(min=1)], widget=NumberInput())
	price = IntegerField('Price', render_kw={'readonly':'True'})
	submit = SubmitField('Book')
'''
