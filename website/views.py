from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Personaldiary
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		diary = request.form.get('diary')

		diary = []
		if not diary:
			diary.append({'title': 'My first entry', 'date': '2022-03-03', 'body': 'This is my first diary entry'})
		else:
			new_entry = Personaldiary(title=form.title.data, body=form.body.data, date=datetime.now())
			diary.append(new_entry)
			
		if 	len(diary) < 1:
			flash('Note is too short!', category='error')
		else:
			new_entry = Personaldiary(title=diary, date=diary, body=diary, user_id=current_user.id)
			db.session.add(new_entry)
			db.session.commit()
			flash('Successfully Saved', category='success')

	return render_template("home.html", user=current_user)