from dateutil.parser import parse
from app import app, db, query
from app.models import User, Staff, Event, EventSlot
from app.forms import MemberLoginForm, AdminLoginForm, RegistrationForm, SearchForm
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Events Booking System')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
	# if already logged in redirect to homepage
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = MemberLoginForm()
	if form.validate_on_submit():
		# if login is successful, return user to 'index'
		user = User.query.filter_by(username=form.username.data).first()
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))

	# render login page
	return render_template('login.html', title='Sign In', form=form)


@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
	# if already logged in redirect to homepage
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = AdminLoginForm()
	if form.validate_on_submit():
		staff = Staff.query.filter_by(username=form.username.data).first()
		login_user(staff, remember=form.remember_me.data)
		#redirect to admin page using flask_admin(endpoint=admin)
		return redirect(url_for('admin.index'))

	# renders staff login page
	return render_template('staff_login.html', title='Admin Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	# if already logged in redirect to homepage
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('index'))
	return render_template('register.html', page_title='Account Registration', form=form)


@app.route('/event')
def show_events():
	return redirect(url_for('search_option', option='title'))


@app.route('/event/<option>', methods=['GET', 'POST'])
def search_option(option):
	form = SearchForm()
	form.search_type.data = option
	if option == 'date':
		form.search_field = form.DATE_FIELD
	elif option == 'price':
		form.search_field = form.PRICE_FIELD

	if form.is_submitted():
		search_type = form.search_type.data
		keyword = str(form.search_field.data).strip()
		if len(keyword) > 0:
			return render_template('event.html', title='Events', form=form,
								   event_list=get_events(search_type, keyword))

	return render_template('event.html', title='Events',
						   form=form, event_list=get_events())


@app.route('/event/details')
def show_details():
	return redirect(url_for('event_details', eid='1'))


@app.route('/event/details/<eid>')
def event_details(eid):
	records = db.session.query(Event, EventSlot).\
				join(EventSlot, Event.event_id == EventSlot.event_id).\
				filter(Event.event_id == eid).all()
	event = query.format_events(records)[0]
	return render_template('details.html', page_title='Test event details page', event=event)
### to understand how an event data is structured, scroll down to format_events function


########################
# SUPPORTING FUNCTIONS #
########################

def get_events(search_type=None, keyword=None):
	if keyword is None:
		return query.query_all()
	elif search_type == 'title':
		return query.title_query(keyword)
	elif search_type == 'type':
		return query.type_query(keyword)
	elif search_type == 'date':
		return query.date_query(keyword)
	else:
		return query.price_query(keyword)
