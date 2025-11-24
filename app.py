from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import os
from mail_config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

db = SQLAlchemy(app)
mail = Mail(app)

# Database Model for Contact Messages
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

# WTForm for Contact
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Courses data (dynamic list)
courses = [
    {'title': 'Data Science', 'icon': 'data-science-icon.png', 'duration': '4 Months', 'instructor': 'Alex Johnson', 'description': 'Dive into data analysis, machine learning, and big data tools.'},
    {'title': 'Python Full Stack', 'icon': 'python-icon.png', 'duration': '6 Months', 'instructor': 'John Doe', 'description': 'Learn full-stack development with Python, Flask/Django, and frontend tech.'},
    {'title': 'Java Full Stack', 'icon': 'java-icon.png', 'duration': '6 Months', 'instructor': 'Jane Smith', 'description': 'Master Java, Spring Boot, and full-stack web development.'},
    # {'title': 'Data Science', 'icon': 'data-science-icon.png', 'duration': '4 Months', 'instructor': 'Alex Johnson', 'description': 'Dive into data analysis, machine learning, and big data tools.'},
    {'title': 'Generative AI', 'icon': 'gen-ai-icon.png', 'duration': '3 Months', 'instructor': 'Emily Davis', 'description': 'Explore AI models like GPT, image generation, and ethical AI.'},
    {'title': 'AWS & DevOps', 'icon': 'aws-devops-icon.png', 'duration': '5 Months', 'instructor': 'Michael Brown', 'description': 'Cloud computing with AWS, CI/CD, Docker, and Kubernetes.'}
]

@app.route('/')
def index():
    return render_template('index.html', courses=courses[:3])  # Show top 3 in carousel

@app.route('/courses')
def courses_page():
    return render_template('courses.html', courses=courses)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    msg=None
    if form.validate_on_submit():
        # Store in DB
        new_message = ContactMessage(name=form.name.data, email=form.email.data, subject=form.subject.data, message=form.message.data)
        db.session.add(new_message)
        db.session.commit()
        
        # Send email
        msg = Message(subject=form.subject.data, recipients=[ADMIN_EMAIL])
        msg.body = f"New message from {form.name.data} ({form.email.data}):\n\n{form.message.data}"
        try:
            mail.send(msg)
            msg='Your message has been sent successfully!'
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'danger')
        
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form,msg=msg)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create DB tables if not exist
    app.run(debug=True)