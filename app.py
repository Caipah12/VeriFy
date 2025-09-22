from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_bcrypt import Bcrypt
import MySQLdb
from flask_mail import Mail, Message
import random, string
import requests
from forms import ForgotPasswordForm
from datetime import datetime, timedelta
from forms import ResetPasswordForm
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.news_model import NewsModel  # Import the NewsModel class
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import csv
import os
import subprocess
from nbconvert.preprocessors import ExecutePreprocessor
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
import nbformat
from nbformat import v4 as nbf
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import current_app as app
import threading
from flask_mail import Mail
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import MySQLdb
import os
import random, string
from datetime import datetime, timedelta
from dotenv import load_dotenv
from datetime import datetime, timedelta  # Change this line if you have it different
from flask_mail import Message
import random
import string
from datetime import datetime, timedelta
import json
import MySQLdb.cursors
from flask import session, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask import jsonify
from itsdangerous import URLSafeTimedSerializer
import uuid
from datetime import datetime, timedelta
from flask import redirect, url_for, flash
from models.model_trainer import fast_train_model, save_model # type: ignore
import os
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
import requests
from functools import wraps
from flask import request, flash, redirect, url_for
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret keys for Flask app and reCAPTCHA
app.config['SECRET_KEY'] = 'iamtomel'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfPEjsqAAAAADQxx2sR1It79r22NC4LAdyrQ0qp'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfPEjsqAAAAAHWMi7l7etJ-fe3rzXkJwWV-uTOe'

# Mail setup with App Password
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ifahsha04@gmail.com'
app.config['MAIL_PASSWORD'] = 'rqca xsca fjca nqwi'
PREFERRED_URL_SCHEME='http'
# App Password here
mail = Mail(app)

import MySQLdb
import MySQLdb.cursors
import traceback
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

# Initialize bcrypt
bcrypt = Bcrypt(app)

def get_db_connection():
    try:
        connection = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="root",
            db="verifydata_db",
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        print("Database connection successful")
        return connection
    except MySQLdb.Error as e:
        print(f"Database connection error: {e}")
        traceback.print_exc()
        return None


# Import the NewsModel class from the models directory
from models.news_model import NewsModel

# Instantiate the NewsModel with your correct paths
news_model = NewsModel(
    model_path=r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\best_news_model.pkl",
    dataset_path=r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\news_model.csv"
)

# File paths based on your specified paths
DATASET_CSV = r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\news_model.csv"
SAMPLE_CSV = r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\Sample\Sample_CSV.csv"
TEMP_DATASET_CSV = r'C:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\temp_dataset.csv'

# Paths to the notebook, model, and dataset
NOTEBOOK_PATH = "C:/Users/ifahs/OneDrive/Documents/FYP_Interface/Fake_News_Detection-master (1)/Fake_News_Detection-master/Fake_News_Detection.ipynb"
MODEL_PATH = "c:/Users/ifahs/OneDrive/Documents/FYP_Interface/models/best_news_model.pkl"
DATASET_PATH = "c:/Users/ifahs/OneDrive/Documents/FYP_Interface/models/news_model.csv"
SAMPLE_CSV_PATH = "C:/Users/ifahs/OneDrive/Documents/FYP_Interface/Sample/Sample_CSV.csv"


def query_db(query, args=(), one=False):
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        cursor.close()
        return (rv[0] if rv else None) if one else rv

# Create the Login form class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', message="Password must have uppercase, lowercase, a number, and a special character.")
    ])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).+$', 
               message="Password must have at least one uppercase, one lowercase, one digit, and one special character.")
    ])
    submit = SubmitField('Sign Up')


# Function to get user by ID
def get_user_by_id(user_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        return cursor.fetchone()

# Function to store reset token in the database
def store_reset_token(user_id, reset_token):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("UPDATE users SET reset_token=%s WHERE id=%s", (reset_token, user_id))
        db.commit()

# Function to get user by reset token
def get_user_by_token(token):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE reset_token=%s", (token,))
        return cursor.fetchone()

# Function to update the user's password
def update_user_password(user_id, hashed_password):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("UPDATE users SET password=%s, reset_token=NULL WHERE id=%s", (hashed_password, user_id))
        db.commit()


# Initialize serializer for token generation
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
        return email
    except:
        return False


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Get the reCAPTCHA response token
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not recaptcha_response:
            flash('Please complete the CAPTCHA.', 'danger')
            return redirect(url_for('login'))

        # Verify reCAPTCHA
        data = {
            'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': recaptcha_response
        }
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        response = requests.post(verify_url, data=data)
        result = response.json()

        if not result.get('success'):
            flash('Captcha verification failed. Please try again.', 'danger')
            return redirect(url_for('login'))

        try:
            # Database connection
            db = get_db_connection()
            if not db:
                flash('Database connection error.', 'danger')
                return redirect(url_for('login'))

            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            
            print(f"Attempting login for email: {email}")
            
            cursor.execute(
                "SELECT id, email, password, role, status, username FROM users WHERE email = %s", 
                (email,)
            )
            user = cursor.fetchone()
            
            print(f"Found user data: {user}")

            if user and bcrypt.check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['user_role'] = user['role']
                session['username'] = user['username']  # Store username in session
                
                cursor.execute(
                    "UPDATE users SET last_login = NOW() WHERE id = %s",
                    (user['id'],)
                )
                db.commit()

                print(f"Login successful. Role: {user['role']}")
                
                if user['role'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('main'))
            else:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login'))

        except Exception as e:
            print(f"Login error: {e}")
            traceback.print_exc()
            flash('An error occurred during login. Please try again.', 'danger')
            return redirect(url_for('login'))
            
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'db' in locals() and db:
                db.close()

    return render_template('login.html', form=form)

# Setup MySQL connection
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="verifydata_db")
cursor = db.cursor()

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get reCAPTCHA response
        recaptcha_response = request.form.get('g-recaptcha-response')
        if not recaptcha_response:
            flash('Please complete the reCAPTCHA.', 'error')
            return render_template('register.html', form=form)
            
        # Verify reCAPTCHA
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
            'response': recaptcha_response
        }
        
        try:
            response = requests.post(verify_url, data=data)
            result = response.json()
            
            if not result.get('success'):
                flash('reCAPTCHA verification failed. Please try again.', 'error')
                return render_template('register.html', form=form)
            
            db = get_db_connection()
            cursor = db.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (form.email.data,))
            if cursor.fetchone():
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('register.html', form=form)

            # Generate verification token
            verification_token = str(uuid.uuid4())
            token_expiry = datetime.now() + timedelta(hours=24)
            
            # Hash password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # Insert new user
            cursor.execute(
                """INSERT INTO users 
                   (username, email, password, role, status, verification_token, token_expiry, email_verified) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (form.username.data, form.email.data, hashed_password, 'user', 'inactive', 
                 verification_token, token_expiry, False)
            )
            db.commit()

            # Send verification email
            verify_url = url_for('verify_email', 
                               token=verification_token, 
                               _external=True)

            msg = Message(
                'Verify Your Email - VeriFy',
                sender=app.config['MAIL_USERNAME'],
                recipients=[form.email.data]
            )
            
            msg.html = render_template(
                'email/verify_email.html',
                verify_url=verify_url,
                username=form.username.data,
                token=verification_token
            )
            
            mail.send(msg)

            flash('Registration successful! Please check your email to verify your account.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            print(f"Registration error: {e}")
            if db:
                db.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    return render_template('register.html', form=form)

@app.route('/verify-email/<token>')
def verify_email(token):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        current_time = datetime.now()
        
        # Update the query to check expiration
        cursor.execute("""
            SELECT id, email, token_expiry 
            FROM users 
            WHERE verification_token = %s 
            AND email_verified = FALSE
            AND token_expiry > %s
        """, (token, current_time))
        
        user = cursor.fetchone()
        
        if not user:
            flash('Invalid or expired verification link.', 'danger')
            return redirect(url_for('login'))
            
        # Update user verification status
        cursor.execute("""
            UPDATE users 
            SET email_verified = TRUE,
                verification_token = NULL,
                token_expiry = NULL,
                status = 'active'
            WHERE id = %s
        """, (user['id'],))
        
        db.commit()
        flash('Email verified successfully! You can now login.', 'success')
        
    except Exception as e:
        print(f"Verification error: {e}")
        flash('An error occurred during verification. Please try again.', 'danger')
        
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
            
    return redirect(url_for('login'))

@app.route('/resend-verification')
def resend_verification():
    if 'email' not in session:
        flash('Please provide your email address.', 'danger')
        return redirect(url_for('login'))
        
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Get user details
        cursor.execute("""
            SELECT id, username, email_verified 
            FROM users 
            WHERE email = %s
        """, (session['email'],))
        
        user = cursor.fetchone()
        
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('login'))
            
        if user['email_verified']:
            flash('Email already verified.', 'info')
            return redirect(url_for('login'))
            
        # Generate new verification token
        new_token = str(uuid.uuid4())
        token_expiry = datetime.now() + timedelta(hours=24)
        
        # Update user with new token
        cursor.execute("""
            UPDATE users 
            SET verification_token = %s,
                token_expiry = %s
            WHERE id = %s
        """, (new_token, token_expiry, user['id']))
        
        db.commit()
        
        # Send new verification email
        verify_url = url_for('verify_email', token=new_token, _external=True)
        msg = Message(
            'Verify Your Email - VeriFy',
            sender=app.config['MAIL_USERNAME'],
            recipients=[session['email']]
        )
        msg.html = render_template(
            'email/verify_email.html',
            verify_url=verify_url,
            username=user['username']
        )
        mail.send(msg)
        
        flash('A new verification email has been sent. Please check your inbox.', 'success')
        
    except Exception as e:
        print(f"Resend verification error: {e}")
        flash('An error occurred. Please try again.', 'danger')
        
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
            
    return redirect(url_for('login'))

# Add this function at the top with your other functions
def test_mail_connection(mail):
    try:
        with mail.connect() as conn:
            return True
    except Exception as e:
        print(f"Mail connection error: {e}")
        return False

# First, update your imports at the top of the file
from datetime import datetime, timedelta  # Change this line if you have it different
from flask_mail import Message
import random
import string

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        try:
            email = form.email.data
            
            # First, check if the mail server is connected
            if not test_mail_connection(mail):
                flash('Error connecting to mail server. Please try again later.', 'danger')
                return redirect(url_for('forgot_password'))
            
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                # Generate reset token and expiry
                reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                reset_token_expiry = datetime.now() + timedelta(hours=1)  # Fixed this line
                
                # Update database with token and expiry
                cursor.execute(
                    "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE email = %s",
                    (reset_token, reset_token_expiry, email)
                )
                db.commit()
                
                # Generate reset URL
                reset_url = url_for('reset_with_token', token=reset_token, _external=True)
                
                # Create email message
                msg = Message(
                    subject='Password Reset Request',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email]
                )
                
                # Email body
                msg.body = f"""Hello,

You have requested to reset your password. Please click on the following link to reset your password:

{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
VeriFy Team
"""
                
                # HTML version of the email
                msg.html = f"""
                <h2>Password Reset Request</h2>
                <p>Hello,</p>
                <p>You have requested to reset your password. Please click on the following link to reset your password:</p>
                <p><a href="{reset_url}">Click here to reset your password</a></p>
                <p>Or copy and paste this URL into your browser:</p>
                <p>{reset_url}</p>
                <p>This link will expire in 1 hour.</p>
                <p>If you did not request this password reset, please ignore this email.</p>
                <p>Best regards,<br>VeriFy Team</p>
                """
                
                try:
                    mail.send(msg)
                    flash('Password reset instructions have been sent to your email.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    print(f"Error sending email: {e}")
                    db.rollback()
                    cursor.execute(
                        "UPDATE users SET reset_token = NULL, reset_token_expiry = NULL WHERE email = %s",
                        (email,)
                    )
                    db.commit()
                    flash('Error sending email. Please try again later.', 'danger')
            else:
                # Don't reveal if email exists or not for security
                flash('If an account exists with this email, you will receive password reset instructions.', 'info')
                
        except Exception as e:
            print(f"Error in forgot_password route: {e}")
            flash('An error occurred. Please try again later.', 'danger')
            
    return render_template('forgot_password.html', form=form)

# Also make sure your reset_with_token route uses the correct datetime
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    form = ResetPasswordForm()
    
    try:
        # Check if token exists and is not expired
        current_time = datetime.now()
        cursor.execute(
            "SELECT * FROM users WHERE reset_token = %s AND reset_token_expiry > %s",
            (token, current_time)
        )
        user = cursor.fetchone()

        if not user:
            flash('The password reset link is invalid or has expired.', 'danger')
            return redirect(url_for('forgot_password'))

        if form.validate_on_submit():
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # Update the user's password and clear the reset token
            cursor.execute(
                """UPDATE users 
                   SET password = %s, 
                       reset_token = NULL, 
                       reset_token_expiry = NULL 
                   WHERE reset_token = %s""",
                (hashed_password, token)
            )
            db.commit()
            
            flash('Your password has been updated! You can now login with your new password.', 'success')
            return redirect(url_for('login'))

        return render_template('reset_password.html', form=form, token=token)
        
    except Exception as e:
        print(f"Error in reset_with_token route: {e}")
        flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('login'))



@app.route('/manage_user')
def manage_user():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash('You must be an admin to access this page.', 'danger')
        return redirect(url_for('login'))

    try:
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id, username, email, role, status, last_login
            FROM users
            ORDER BY id DESC
        """)
        
        users = cursor.fetchall()
        
        # Format last_login dates
        for user in users:
            if user['last_login']:
                user['last_login'] = user['last_login'].strftime('%Y-%m-%d %H:%M:%S')
        
        return render_template('manage_user.html', users=users)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('admin'))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/api/user/<int:user_id>')
def get_user_details(user_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("""
            SELECT id, username, email, role, status, last_login
            FROM users
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if user:
            if user['last_login']:
                user['last_login'] = user['last_login'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify(user)
        return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/api/user/<int:user_id>/toggle-status', methods=['POST'])
def toggle_user_status(user_id):
    if 'user_role' not in session or session['user_role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # First get current status
        cursor.execute("SELECT status FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'User not found'}), 404
            
        new_status = 'inactive' if result[0] == 'active' else 'active'
        
        cursor.execute(
            "UPDATE users SET status = %s WHERE id = %s",
            (new_status, user_id)
        )
        db.commit()
        
        return jsonify({'success': True, 'new_status': new_status})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



def get_statistics():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        if not db:
            print("Failed to connect to database")
            return None
            
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        print("Database connection established successfully")

        # Get total articles count
        cursor.execute("SELECT COUNT(*) as total FROM articles")
        total_result = cursor.fetchone()
        print(f"Total result: {total_result}")  # Debug print
        total_articles = total_result['total'] if total_result else 0
        
        # Get fake vs real news counts
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN is_fake = 1 THEN 1 ELSE 0 END) as fake_count,
                SUM(CASE WHEN is_fake = 0 THEN 1 ELSE 0 END) as real_count
            FROM articles
        """)
        counts = cursor.fetchone()
        print(f"Counts result: {counts}")  # Debug print
        
        # Get trend data for the last 7 days
        cursor.execute("""
            SELECT 
                DATE(created_at) as date,
                SUM(CASE WHEN is_fake = 1 THEN 1 ELSE 0 END) as fake_count,
                SUM(CASE WHEN is_fake = 0 THEN 1 ELSE 0 END) as real_count
            FROM articles
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        trend_data = cursor.fetchall()
        print(f"Trend data: {trend_data}")  # Debug print
        
        # Format the trend data for the chart
        dates = []
        fake_trend = []
        real_trend = []
        
        current_date = datetime.now().date()
        for i in range(6, -1, -1):
            date = (current_date - timedelta(days=i)).strftime('%Y-%m-%d')
            dates.append(date)
            
            # Find matching data or use 0
            matching_data = next(
                (row for row in trend_data if row['date'].strftime('%Y-%m-%d') == date),
                {'fake_count': 0, 'real_count': 0}
            )
            
            fake_trend.append(int(matching_data['fake_count'] or 0))
            real_trend.append(int(matching_data['real_count'] or 0))
        
        statistics = {
            'total_articles': int(total_articles),
            'fake_count': int(counts['fake_count'] or 0) if counts else 0,
            'real_count': int(counts['real_count'] or 0) if counts else 0,
            'trend_data': {
                'dates': dates,
                'fake_trend': fake_trend,
                'real_trend': real_trend
            }
        }
        
        print(f"Final statistics: {statistics}")  # Debug print
        return statistics

    except Exception as e:
        print(f"Error getting statistics: {e}")
        traceback.print_exc()  # This will print the full error traceback
        return {
            'total_articles': 0,
            'fake_count': 0,
            'real_count': 0,
            'trend_data': {
                'dates': [],
                'fake_trend': [],
                'real_trend': []
            }
        }
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/debug_articles')
def debug_articles():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        # Check total count
        cursor.execute("SELECT COUNT(*) as total FROM articles")
        total = cursor.fetchone()
        
        # Check recent articles
        cursor.execute("""
            SELECT id, user_id, content, is_fake, created_at 
            FROM articles 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent = cursor.fetchall()
        
        return {
            'total_count': total,
            'recent_articles': recent
        }
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    
# Update the main route to handle None statistics
@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    try:
        stats = get_statistics()
        if stats is None:
            stats = {
                'total_articles': 0,
                'fake_count': 0,
                'real_count': 0,
                'unsure_count': 0,
                'trend_data': {
                    'dates': [],
                    'fake_trend': [],
                    'real_trend': []
                }
            }
        return render_template('main.html', 
                             stats=stats, 
                             username=session.get('username', 'Guest'))
    except Exception as e:
        print(f"Error in main route: {e}")
        return render_template('main.html', 
                             error="An error occurred loading statistics.",
                             username=session.get('username', 'Guest'))

@app.route('/submit_article', methods=['POST'])
def submit_article():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    article_content = request.form.get('news_content', '')
    
    try:
        # Changed from .prediction to .predict
        prediction, confidence_score, similar_articles = news_model.predict(article_content)
        
        # Save to database with original text
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute(
            """INSERT INTO articles 
               (user_id, content, is_fake, confidence_score, created_at) 
               VALUES (%s, %s, %s, %s, NOW())""",
            (session['user_id'], article_content, 
             1 if prediction == 'Fake' else 0, float(confidence_score))
        )
        db.commit()

        stats = get_statistics()
        
        return render_template(
            'main.html',
            prediction=prediction,
            confidence_score=confidence_score,
            similar_articles=similar_articles,
            stats=stats,
            datetime=datetime
        )

    except ValueError as e:
        flash(str(e), 'warning')
        stats = get_statistics()
        return render_template('main.html', stats=stats)
        
    except Exception as e:
        print(f"Error in submit_article: {e}")
        traceback.print_exc()
        flash("An error occurred during analysis.", 'danger')
        stats = get_statistics()
        return render_template('main.html', stats=stats)
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
    




@app.route('/admin')
def admin():
    if 'user_role' not in session or session['user_role'] != 'admin':
        flash("You need to log in as an admin to access the dashboard.", 'danger')
        return redirect(url_for('login'))

    try:
        db = get_db_connection()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor here

        # Initialize variables with default values
        user_submissions = 0
        total_articles = 0
        flagged_as_fake = 0
        unsure_articles = 0
        last_trained = 'N/A'
        model_status = 'N/A'
        fake_articles = []

        # Get user submissions count
        cursor.execute("SELECT COUNT(*) as count FROM submissions")
        result = cursor.fetchone()
        user_submissions = result['count'] if result else 0

        # Get total articles count
        cursor.execute("SELECT COUNT(*) as count FROM articles")
        result = cursor.fetchone()
        total_articles = result['count'] if result else 0

        # Get fake news count (where is_fake = 2)
        cursor.execute("SELECT COUNT(*) as count FROM articles WHERE is_fake = 2")
        result = cursor.fetchone()
        flagged_as_fake = result['count'] if result else 0

        # Get unsure articles count (where is_fake = 0)
        cursor.execute("SELECT COUNT(*) as count FROM articles WHERE is_fake = 0")
        result = cursor.fetchone()
        unsure_articles = result['count'] if result else 0

        # Get fake articles for the modal
        cursor.execute("""
            SELECT id, content, created_at 
            FROM articles 
            WHERE is_fake = 1 
            ORDER BY created_at DESC
        """)
        fake_articles = cursor.fetchall()  # With DictCursor, this will return dicts

        # Get model status
        try:
            cursor.execute("SELECT last_trained, status FROM model_status ORDER BY id DESC LIMIT 1")
            model_result = cursor.fetchone()
            if model_result:
                last_trained = model_result['last_trained'].strftime('%Y-%m-%d') if model_result['last_trained'] else 'N/A'
                model_status = model_result['status'] if model_result['status'] else 'N/A'
        except Exception as e:
            print(f"Error fetching model status: {e}")
            # Continue with default values if this fails

        print(f"Debug - Stats: submissions={user_submissions}, articles={total_articles}, fake={flagged_as_fake}, unsure={unsure_articles}")

        return render_template(
            'admin.html',
            user_submissions=user_submissions,
            total_articles=total_articles,
            flagged_as_fake=flagged_as_fake,
            last_trained=last_trained,
            model_status=model_status,
            fake_articles=fake_articles
        )

    except Exception as e:
        print(f"Error in admin dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        flash("An error occurred loading the dashboard.", 'danger')
        return redirect(url_for('login'))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

@app.route('/manage_dataset')
def manage_dataset():
    articles = []
    try:
        with open(TEMP_DATASET_CSV, 'r', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            articles = list(reader)
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error loading temporary dataset: {e}")

    return render_template('manage_dataset.html', articles=articles)

@app.route('/add_data', methods=['POST'])
def add_data():
    title = request.form['title']
    text = request.form['text']
    subject = request.form['subject']
    date = request.form['date']
    label = request.form['label']

    # Generate a new unique ID based on the data in news_model.csv
    next_id = 1  # Start with 1 if news_model.csv is empty
    try:
        # Read the existing data from news_model.csv to find the highest ID
        with open(DATASET_CSV, 'r', encoding='ISO-8859-1') as file:  # Use ISO-8859-1 encoding
            reader = csv.DictReader(file)
            ids = [int(row['id']) for row in reader if 'id' in row and row['id'].isdigit()]
            if ids:
                next_id = max(ids) + 1  # Increment the highest ID found
    except FileNotFoundError:
        # If the file does not exist, start with ID 1
        pass

    # Create the new row with the generated ID
    row = {'id': next_id, 'title': title, 'text': text, 'subject': subject, 'date': date, 'label': label}

    # Append data to both news_model.csv and temp_dataset.csv
    with open(TEMP_DATASET_CSV, 'a', newline='', encoding='utf-8') as temp_file, open(DATASET_CSV, 'a', newline='', encoding='utf-8') as main_file:
        fieldnames = ['id', 'title', 'text', 'subject', 'date', 'label']
        temp_writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        main_writer = csv.DictWriter(main_file, fieldnames=fieldnames)
        
        # Write headers if the files are empty
        if os.path.getsize(TEMP_DATASET_CSV) == 0:
            temp_writer.writeheader()
        if os.path.getsize(DATASET_CSV) == 0:
            main_writer.writeheader()

        # Append the row to both files
        temp_writer.writerow(row)
        main_writer.writerow(row)

    flash("New labeled data added successfully!", 'success')
    return redirect(url_for('manage_dataset'))


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('manage_dataset'))

    file = request.files['csv_file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('manage_dataset'))

    try:
        # Determine the next unique ID based on the data in news_model.csv
        next_id = 1
        try:
            with open(DATASET_CSV, 'r', encoding='ISO-8859-1') as f:
                reader = csv.DictReader(f)
                ids = [int(row['id']) for row in reader if 'id' in row and row['id'].isdigit()]
                if ids:
                    next_id = max(ids) + 1  # Increment the highest ID found
        except FileNotFoundError:
            # If the file does not exist, start with ID 1
            pass

        # Open both files for appending and write new data with unique IDs
        with open(TEMP_DATASET_CSV, 'a', newline='', encoding='utf-8') as temp_file, open(DATASET_CSV, 'a', newline='', encoding='utf-8') as main_file:
            fieldnames = ['id', 'title', 'text', 'subject', 'date', 'label']
            temp_writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            main_writer = csv.DictWriter(main_file, fieldnames=fieldnames)

            # Write headers if the files are empty
            if os.path.getsize(TEMP_DATASET_CSV) == 0:
                temp_writer.writeheader()
            if os.path.getsize(DATASET_CSV) == 0:
                main_writer.writeheader()

            # Read and process the uploaded CSV file
            file.seek(0)  # Reset the file pointer
            csv_reader = csv.reader(file.read().decode('utf-8').splitlines())
            next(csv_reader)  # Skip the header of the uploaded CSV
            for row in csv_reader:
                # Ensure the row has the expected number of columns
                if len(row) < 5:
                    print("Skipping row due to insufficient columns:", row)
                    continue

                new_row = {
                    'id': next_id,
                    'title': row[0],
                    'text': row[1],
                    'subject': row[2],
                    'date': row[3],
                    'label': row[4]
                }
                temp_writer.writerow(new_row)
                main_writer.writerow(new_row)
                next_id += 1  # Increment the ID for the next row

        flash('CSV data uploaded successfully!', 'success')
    except Exception as e:
        print(f"Error: {e}")
        flash(f'Error uploading CSV data: {e}', 'danger')

    return redirect(url_for('manage_dataset'))


@app.route('/edit_data/<int:id>', methods=['POST'])
def edit_data(id):
    try:
        # Retrieve updated data from the form
        title = request.form['title']
        text = request.form['text']
        subject = request.form['subject']
        date = request.form['date']
        label = request.form['label']

        updated_row = {
            'id': str(id),
            'title': title,
            'text': text,
            'subject': subject,
            'date': date,
            'label': label
        }

        def update_row_in_file(file_path, row_id, updated_row):
            temp_file_path = file_path + '.tmp'
            rows = []
            try:
                # First read all rows
                with open(file_path, 'r', encoding='ISO-8859-1') as file:
                    reader = csv.DictReader(file)
                    fieldnames = reader.fieldnames
                    for row in reader:
                        if row.get('id') == str(row_id):
                            rows.append(updated_row)
                        else:
                            rows.append(row)

                # Then write all rows back
                with open(temp_file_path, 'w', newline='', encoding='ISO-8859-1') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                # Replace original file with temporary file
                os.replace(temp_file_path, file_path)
                return True

            except Exception as e:
                print(f"Error updating {file_path}: {str(e)}")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                return False

        # Update both files
        temp_success = update_row_in_file(TEMP_DATASET_CSV, id, updated_row)
        main_success = update_row_in_file(DATASET_CSV, id, updated_row)

        if temp_success and main_success:
            flash("Data updated successfully!", 'success')
        else:
            flash("Error updating data in one or both files.", 'danger')
        
        return redirect(url_for('manage_dataset'))

    except Exception as e:
        flash(f"Error updating data: {str(e)}", 'danger')
        return redirect(url_for('manage_dataset'))
    
@app.route('/delete_data/<int:id>', methods=['POST'])
def delete_data(id):
    def delete_row_in_file(file_path, row_id):
        try:
            # Read all rows from the file
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                # Ensure we only delete the row with the exact matching ID
                rows = []
                for row in reader:
                    if 'id' in row and row['id'].isdigit():
                        if int(row['id']) != row_id:
                            rows.append(row)  # Keep rows that do not match the ID

            # Write the filtered rows back to the file
            with open(file_path, 'w', newline='', encoding='ISO-8859-1') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"Error deleting from {file_path}: {e}")
            flash(f"Error deleting from {file_path}: {e}", 'danger')

    # Delete the row in both temp_dataset.csv and news_model.csv
    delete_row_in_file(TEMP_DATASET_CSV, id)
    delete_row_in_file(DATASET_CSV, id)

    flash("Data deleted successfully!", 'success')
    return redirect(url_for('manage_dataset'))



# Route: Download Sample CSV
@app.route('/download_sample_csv')
def download_sample_csv():
    return send_file(SAMPLE_CSV, as_attachment=True)

@app.route('/logout')
def logout():
    # Delete the temporary dataset file on logout
    if os.path.exists(TEMP_DATASET_CSV):
        os.remove(TEMP_DATASET_CSV)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))





@app.route('/')
def dashboard():
    # Fetch the latest model status
    last_trained = session.get('last_trained', 'N/A')
    model_status = session.get('model_status', 'Not Trained')
    return render_template('dashboard.html', last_trained=last_trained, model_status=model_status)

def execute_notebook_cells(notebook_path, output_path):
    """Execute notebook cells one by one with detailed logging"""
    print(f"Starting notebook execution from: {notebook_path}")
    
    try:
        # Update progress - Loading notebook
        training_progress.update(10, "Loading notebook")
        
        # Load the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Update progress - Configuring paths    
        training_progress.update(20, "Configuring paths")
            
        # Modify the save path in the notebook before execution
        for cell in nb.cells:
            if cell.cell_type == "code" and "save_path =" in cell.source:
                cell.source = cell.source.replace(
                    'save_path = r"C:\\Users\\ifahs\\OneDrive\\Documents\\FYP_Interface\\models"',
                    f'save_path = r"c:\\Users\\ifahs\\OneDrive\\Documents\\FYP_Interface\\models\\best_news_model.pkl"'
                )
        
        # Update progress - Creating preprocessor
        training_progress.update(30, "Initializing training environment")
        
        # Create the preprocessor
        ep = ExecutePreprocessor(
            timeout=1800,
            kernel_name='python3',
            allow_errors=False
        )
        
        # Create output path if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Create a new notebook for output
        output_notebook = os.path.join(output_path, 'executed_notebook.ipynb')
        
        # Update progress - Starting execution
        training_progress.update(40, "Starting model training")
        
        print("Executing notebook...")
        # Execute and capture output
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        # Update progress - Saving results
        training_progress.update(90, "Saving trained model")
        
        # Save executed notebook
        with open(output_notebook, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
            
        # Update progress - Complete
        training_progress.update(100, "Training completed successfully")
        print("Notebook execution completed successfully")
        return True, None
        
    except Exception as e:
        error_msg = f"Notebook execution failed: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        training_progress.update(0, "Training failed", error_msg)
        return False, error_msg

class TrainingProgress:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrainingProgress, cls).__new__(cls)
            cls._instance.progress = 0
            cls._instance.status = "Not Started"
            cls._instance.error = None
            cls._instance.is_training = False
        return cls._instance

    def reset(self):
        self.progress = 0
        self.status = "Not Started"
        self.error = None
        self.is_training = False

    def update(self, progress, status=None, error=None):
        self.progress = progress
        if status:
            self.status = status
        if error:
            self.error = error

@app.route('/get_training_status')
def get_training_status():
    return jsonify({
        'progress': training_progress.progress,
        'status': training_progress.status,
        'error': training_progress.error,
        'is_training': training_progress.is_training
    })


# Create a global instance
training_progress = TrainingProgress()


@app.route('/initiate_training', methods=['POST'])
def initiate_training():
    if training_progress.is_training:
        return jsonify({
            "success": False,
            "error": "Training is already in progress"
        })
    
    db = None
    cursor = None
    try:
        training_progress.reset()
        training_progress.is_training = True
        training_progress.update(0, "Initializing fast training")
        
        # Paths
        data_path = os.path.abspath(r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\news_model.csv")
        model_path = os.path.abspath(r"c:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\best_news_model.pkl")
        
        training_progress.update(20, "Loading data")
        
        # Train model with optimized function
        training_progress.update(40, "Training models")
        model, vectorizer = fast_train_model(data_path)
        
        training_progress.update(80, "Saving model")
        save_model(model, vectorizer, model_path)
        
        # Update database
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO model_status (status, last_trained) VALUES (%s, NOW())",
            ("Active",)
        )
        db.commit()
        
        training_progress.update(100, "Training completed")
        
        return jsonify({
            "success": True,
            "message": "Training completed successfully"
        })
        
    except Exception as e:
        error_msg = f"Training error: {str(e)}"
        print(error_msg)
        
        if db and cursor:
            try:
                cursor.execute(
                    "INSERT INTO model_status (status, last_trained, error_message) VALUES (%s, NOW(), %s)",
                    ("Error", str(e))
                )
                db.commit()
            except Exception as db_error:
                print(f"Error updating status: {db_error}")
        
        return jsonify({
            "success": False,
            "error": str(e)
        })
        
    finally:
        training_progress.is_training = False
        if cursor:
            cursor.close()
        if db:
            db.close()


@app.route('/manage_model')
def manage_model():
    db = None
    cursor = None
    try:
        db = get_db_connection()
        if not db:
            raise Exception("Failed to connect to database")
            
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        # Get latest model status
        cursor.execute("""
            SELECT status, last_trained 
            FROM model_status 
            ORDER BY id DESC LIMIT 1
        """)
        
        result = cursor.fetchone()
        
        model_status = result['status'] if result else 'Not Trained'
        # Format the time to include hours, minutes and seconds
        if result and result['last_trained']:
            last_trained = result['last_trained'].strftime('%Y-%m-%d')
        else:
            last_trained = 'Never'

        return render_template('manage_model.html', 
                             model_status=model_status,
                             last_trained=last_trained)
                             
    except Exception as e:
        print(f"Error in manage_model route: {e}")
        return render_template('manage_model.html',
                             model_status='Error',
                             last_trained='Never')
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

# Add debug route to check file paths and permissions
@app.route('/debug/model_paths')
def debug_model_paths():
    try:
        paths = {
            'notebook_path': os.path.abspath(r"C:\Users\ifahs\OneDrive\Documents\FYP_Interface\Fake_News_Detection-master (1)\Fake_News_Detection-master\Fake_News_Detection.ipynb"),
            'model_path': os.path.abspath(r"c:\Users\ifahs\OneDrive\Documents\FYP_Interface\models\best_news_model.pkl")
        }
        
        result = {}
        for name, path in paths.items():
            result[name] = {
                'path': path,
                'exists': os.path.exists(path),
                'is_readable': os.access(path, os.R_OK) if os.path.exists(path) else None,
                'is_writable': os.access(os.path.dirname(path), os.W_OK),
                'parent_exists': os.path.exists(os.path.dirname(path))
            }
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        })

def update_model_status(db, status):
    """Helper function to update model status"""
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO model_status (status, last_trained) VALUES (%s, NOW())",
            (status,)
        )
        db.commit()
    except Exception as e:
        print(f"Error updating model status: {e}")
        if db:
            db.rollback()
    finally:
        if cursor:
            cursor.close()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
