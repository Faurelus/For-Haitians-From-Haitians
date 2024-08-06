# app/routes.py
from flask import current_app as app, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required, login_user
from werkzeug.utils import secure_filename
import os
import requests
from app import db, bcrypt
from app.forms import RegistrationForm, ProfileForm
from app.models import User, Profile, Donation
import stripe
import logging

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        profile = Profile(user_id=user.id, first_name='', last_name='', dob=None, address='', phone_number='', profile_pic=None)
        db.session.add(profile)
        db.session.commit()
        flash('Account created!', 'success')
        login_user(user)  # Automatically log in the user after registration
        return redirect(url_for('edit_profile'))
    return render_template('signup.html', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            pic_filename = secure_filename(form.profile_pic.data.filename)
            pic_path = os.path.join(app.config['UPLOAD_FOLDER'], pic_filename)
            form.profile_pic.data.save(pic_path)
            current_user.profile.profile_pic = pic_filename
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.dob = form.dob.data
        current_user.profile.address = form.address.data
        current_user.profile.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.dob.data = current_user.profile.dob
        form.address.data = current_user.profile.address
        form.phone_number.data = current_user.profile.phone_number
    return render_template('edit_profile.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/mission')
def mission():
    return render_template('mission.html')

@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.route('/fundraiser')
def fundraiser():
    return render_template('fundraiser.html')

@app.route('/news')
def news():
    url = f"https://newsdata.io/api/1/news?apikey={app.config['NEWS_API_KEY']}&q=haiti&country=ht"
    response = requests.get(url)
    news_data = response.json()
    return render_template('news.html', news=news_data)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    amount = data.get('amount')
    if not amount:
        return jsonify({'error': 'Amount is required'}), 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'General Donation',
                    },
                    'unit_amount': int(amount) * 100,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/create-fundraiser-session', methods=['POST'])
def create_fundraiser_session():
    data = request.get_json()
    amount = data.get('amount')
    fundraiser_id = data.get('fundraiser_id')
    if not amount or not fundraiser_id:
        return jsonify({'error': 'Amount and Fundraiser ID are required'}), 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Fundraiser Donation {fundraiser_id}',
                    },
                    'unit_amount': int(amount) * 100,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('fundraiser_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}&fundraiser_id=' + fundraiser_id,
            cancel_url=url_for('fundraiser_cancel', _external=True),
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/fundraiser-success')
def fundraiser_success():
    return render_template('fundraiser_success.html')

@app.route('/fundraiser-cancel')
def fundraiser_cancel():
    return render_template('fundraiser_cancel.html')
