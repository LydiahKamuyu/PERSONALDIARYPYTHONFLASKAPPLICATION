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
	default_entry = {
    'title': 'My first entry',
    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'body': 'This is my first diary entry'
}
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

	# Print each diary entry with its date and time/minus microseconds
	for entry in diary_entries:
		entry.date = entry.date.strftime('%Y-%m-%d %H:%M:%S')
		print(f"{entry.body}\n")

	# Combine the default entry with the user's entries
	all_entries = [default_entry] + diary_entries

	return render_template("home.html", user=current_user, diary_entries=diary_entries)

@views.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    # Get the diary entry from the database
    entry = PersonalDiary.query.get_or_404(entry_id)

    # Check if the user is the owner of the diary entry
    if entry.user_id != current_user.id:
        flash('You are not authorized to edit this entry', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        # Get the form data
        form_title = request.form.get('title')
        form_body = request.form.get('body')

        # Check if the form data is valid
        if len(form_title) <= 1 or len(form_body) <= 1:
            flash('Input is too short', category='error')
        else:
            # Update the diary entry with the form data
            entry.title = form_title
            entry.body = form_body
            entry.date = datetime.now()

            # Commit the changes to the database and display a success message
            db.session.commit()
            flash('Successfully updated', category='success')

            return redirect(url_for('views.home'))

    return render_template("edit.html", user=current_user, entry=entry)


@views.route('/delete/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def delete_entry(entry_id):
    # Retrieve the entry with the given entry_id
    entry = PersonalDiary.query.filter_by(id=entry_id).first()

    # Check if the entry exists
    if not entry:
        flash('Entry does not exist.', category='error')
        return redirect(url_for('views.home'))

    # Delete the entry from the database
    db.session.delete(entry)
    db.session.commit()

    flash('Entry deleted successfully!', category='success')
    return redirect(url_for('views.home'))
