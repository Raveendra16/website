from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os
from mail_config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Mail config
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

mail = Mail(app)


@app.context_processor
def inject_globals():
    return {'admin_whatsapp': ADMIN_WHATSAPP}

# Courses data (dynamic list)
courses = [
    {
        'title': 'Data Science with AI',
        'category': 'Data Science',
        'icon': 'fas fa-chart-line',
        'level': 'Intermediate',
        'rating': 4.8,
        'price': 'Contact for Pricing',
        'duration': '4 Months',
        'instructor': 'Alex Johnson',
        'enrolled': '1.8K',
        'lectures': 120,
        'projects': 8,
        'description': 'Dive into data analysis, machine learning, and big data tools.',
        'full_description': 'Master the complete data science lifecycle - from data wrangling and statistical analysis to building and deploying machine learning models - through hands-on projects using real-world datasets.',
        'skills': ['Python for Data Science', 'Statistics & Probability', 'Machine Learning Algorithms', 'Data Visualization', 'SQL & Big Data Tools'],
    },
    {
        'title': 'Python Full Stack',
        'category': 'Web Development',
        'icon': 'fab fa-python',
        'level': 'Beginner',
        'rating': 4.9,
        'price': 'Contact for Pricing',
        'duration': '6 Months',
        'instructor': 'John Doe',
        'enrolled': '2.2K',
        'lectures': 160,
        'projects': 10,
        'description': 'Learn full-stack development with Python, Flask/Django, and frontend tech.',
        'full_description': 'Become a job-ready full-stack developer by mastering Python, Flask and Django on the backend, along with HTML, CSS, JavaScript and React on the frontend, building real production-grade applications.',
        'skills': ['Python & OOP', 'Flask & Django', 'REST APIs', 'HTML, CSS & JavaScript', 'React.js', 'Database Design'],
    },
    {
        'title': 'Java Full Stack',
        'category': 'Web Development',
        'icon': 'fab fa-java',
        'level': 'Intermediate',
        'rating': 4.8,
        'price': 'Contact for Pricing',
        'duration': '6 Months',
        'instructor': 'Jane Smith',
        'enrolled': '2.0K',
        'lectures': 150,
        'projects': 9,
        'description': 'Master Java, Spring Boot, and full-stack web development.',
        'full_description': 'Gain enterprise-grade development skills with Java, Spring Boot and modern frontend frameworks, learning to design, build and deploy scalable full-stack applications.',
        'skills': ['Core & Advanced Java', 'Spring Boot', 'Hibernate & JPA', 'REST APIs', 'React.js', 'Microservices Basics'],
    },
    {
        'title': 'Generative AI',
        'category': 'Artificial Intelligence',
        'icon': 'fas fa-robot',
        'level': 'Advanced',
        'rating': 4.8,
        'price': 'Contact for Pricing',
        'duration': '3 Months',
        'instructor': 'Emily Davis',
        'enrolled': '1.6K',
        'lectures': 90,
        'projects': 6,
        'description': 'Explore AI models like GPT, image generation, and ethical AI.',
        'full_description': 'Explore the cutting edge of AI - large language models, prompt engineering, image generation, and building real applications with tools like LangChain - while understanding responsible AI practices.',
        'skills': ['LLMs & Prompt Engineering', 'LangChain & RAG', 'Image Generation Models', 'Fine-tuning Basics', 'AI Ethics & Safety'],
    },
    {
        'title': 'AWS & DevOps',
        'category': 'Cloud Computing',
        'icon': 'fab fa-aws',
        'level': 'Intermediate',
        'rating': 4.7,
        'price': 'Contact for Pricing',
        'duration': '5 Months',
        'instructor': 'Michael Brown',
        'enrolled': '1.9K',
        'lectures': 130,
        'projects': 8,
        'description': 'Cloud computing with AWS, CI/CD, Docker, and Kubernetes.',
        'full_description': 'Learn to design, deploy and scale cloud infrastructure on AWS, automate delivery pipelines with CI/CD, and containerize applications using Docker and Kubernetes - the core skill set for modern DevOps roles.',
        'skills': ['AWS Core Services (EC2, S3, IAM)', 'Docker & Kubernetes', 'CI/CD Pipelines', 'Infrastructure as Code (Terraform)', 'Monitoring & Logging'],
    },
]

course_titles = [c['title'] for c in courses]


def send_admin_email(subject, body):
    """Send a notification email to the admin. Returns True on success."""
    try:
        msg = Message(subject=subject, recipients=[ADMIN_EMAIL])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f'Email notification failed: {e}')
        return False


def send_thank_you_email(to_email, email_subject, **template_context):
    """Send a designed HTML thank-you email (with embedded logo) to the person who submitted a form."""
    try:
        msg = Message(subject=email_subject, recipients=[to_email])
        msg.body = (
            f"Hi {template_context.get('name')},\n\n"
            "Thank you for reaching out to Bring Back EdTech! We appreciate it and will be in touch soon.\n\n"
            "With gratitude,\nThe Bring Back EdTech Team"
        )
        msg.html = render_template(
            'email/thank_you.html',
            site_url=request.url_root,
            **template_context,
        )
        logo_path = os.path.join(app.root_path, 'static', 'images', 'img.jpg')
        with open(logo_path, 'rb') as f:
            msg.attach('logo.jpg', 'image/jpeg', f.read(), 'inline', headers=[('Content-ID', '<logo>')])
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f'Thank-you email failed: {e}')
        return False


# WTForm for Contact
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=150)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


# WTForm for Enrollment
class EnrollForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    course = SelectField('Course', choices=[(t, t) for t in course_titles], validators=[DataRequired()])
    submit = SubmitField('Enroll Now')


@app.route('/')
def index():
    return render_template('index.html', courses=courses[:3])


@app.route('/courses')
def courses_page():
    enroll_form = EnrollForm()
    return render_template('courses.html', courses=courses, enroll_form=enroll_form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        body = (
            f"New contact message from {form.name.data} ({form.email.data}):\n\n"
            f"Subject: {form.subject.data}\n\n"
            f"{form.message.data}"
        )
        email_sent = send_admin_email(f"New Contact Message: {form.subject.data}", body)
        send_thank_you_email(
            form.email.data,
            'Thank You for Contacting Bring Back EdTech',
            name=form.name.data,
            kind='contact',
            subject=form.subject.data,
            message=form.message.data,
        )

        if email_sent:
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
        else:
            flash('Your message was received, but we could not send a confirmation email. We will still follow up.', 'warning')

        return redirect(url_for('success'))
    return render_template('contact.html', form=form)


@app.route('/enroll', methods=['POST'])
def enroll():
    form = EnrollForm()
    if form.validate_on_submit():
        body = (
            f"New enrollment request:\n\n"
            f"Name: {form.name.data}\n"
            f"Email: {form.email.data}\n"
            f"Phone: {form.phone.data}\n"
            f"Course: {form.course.data}"
        )
        email_sent = send_admin_email(f"New Enrollment: {form.course.data}", body)
        send_thank_you_email(
            form.email.data,
            f'Thank You for Enrolling in {form.course.data}',
            name=form.name.data,
            kind='enroll',
            course=form.course.data,
            phone=form.phone.data,
        )

        if email_sent:
            flash(f"Thanks {form.name.data}! Your enrollment request for {form.course.data} has been received.", 'success')
        else:
            flash('Your enrollment request was received, but we could not send a confirmation email. We will still follow up.', 'warning')

        return redirect(url_for('success'))

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, 'danger')
    return redirect(url_for('courses_page') + '#featured-courses')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
