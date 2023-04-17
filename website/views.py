from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import PersonalDiary
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	# Set up a default diary entry
	default_entry = {'title': 'My first entry', 'date': datetime.now().strftime('%Y-%m-%d'), 'body': 'This is my first diary entry'}
	if request.method == 'POST':
		# Get the form data
		form_title = request.form.get('title')
		form_body = request.form.get('body')

	#checks if the length of either form_title or form_body is less than or equal to 1.
		if len(form_title) <= 1 or len(form_body) <= 1:
			flash('To short', category='error')
		else:

			# Create a new diary entry with the form data
			new_entry = PersonalDiary(title=form_title, body=form_body, date=datetime.now(), user_id=current_user.id)
			
			# Add the new entry to the database and display a success message
			db.session.add(new_entry)
			db.session.commit()
			flash('Successfully Saved', category='success')
			return redirect(url_for('views.home'))

	# Get all diary entries for the current user
	diary_entries = PersonalDiary.query.filter_by(user_id=current_user.id).all()

	# Print each diary entry with its date and time
	for entry in diary_entries:
		print(f"{entry.title} ({entry.date.strftime('%Y-%m-%d %H:%M:%S')})")
		print(f"{entry.body}\n")

	# Combine the default entry with the user's entries
	all_entries = [default_entry] + diary_entries

	return render_template("home.html", user=current_user, diary_entries=diary_entries)
