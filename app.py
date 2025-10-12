from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==========================================
# App Configuration
# ==========================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Da1wi2d$@localhost/hireme"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='oniyonkuru233@gmail.com',
    MAIL_PASSWORD='uhux ycrh jqso vyic',  # Use App Password
    MAIL_DEFAULT_SENDER='oniyonkuru233@gmail.com'
)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)  # ensure app.secret_key exists


# ==========================================
# Initialize Extensions
# ==========================================
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ==========================================
# Database Models
# ==========================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    national_id = db.Column(db.String(16), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('EMPLOYEE', 'EMPLOYER'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = db.relationship('User', backref=db.backref('company', uselist=False))


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(255))
    salary = db.Column(db.String(100))
    type = db.Column(db.Enum('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP'), default='FULL_TIME')
    deadline = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company = db.relationship('Company', backref=db.backref('jobs', lazy=True))


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('APPLIED', 'SHORTLISTED', 'REJECTED', 'HIRED'), default='APPLIED')
    cover_letter = db.Column(db.String(255))
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))


class EmployeeProfile(db.Model):
    __tablename__ = 'employee_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


class EmployeeDocument(db.Model):
    __tablename__ = 'employee_documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    file_type = db.Column(db.Enum('CV', 'DIPLOMA', 'CERTIFICATE'))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('documents', lazy=True))


class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# Create Tables
# ==========================================
with app.app_context():
    db.create_all()
    # Create default admin if not exists
    if not Admin.query.filter_by(email='oniyonkuru210@gmail.com').first():
        admin = Admin(email='oniyonkuru210@gmail.com')
        admin.set_password('Da1wi2d$')
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created: oniyonkuru210@gmail.com / Da1wi2d$")


# ==========================================
# Decorators
# ==========================================
def employer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'EMPLOYER':
            flash('Access denied. Please log in as employer.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def employee_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'EMPLOYEE':
            flash('Access denied. Please log in as employee.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ==========================================
# Helper
# ==========================================
def get_announcements():
    return Announcement.query.order_by(Announcement.created_at.desc()).all()


# ==========================================
# Public Routes
# ==========================================
@app.route('/')
def home():
    featured_jobs = Job.query.order_by(Job.created_at.desc()).limit(3).all()
    announcements = get_announcements()
    return render_template('home.html', featured_jobs=featured_jobs, announcements=announcements)
# ==========================================
# Contact Routes
# ==========================================

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash("All fields are required.", "warning")
        return redirect(request.referrer)

    # Create the email
    msg = Message(
        subject=f"New Contact Form Message from {name}",
        recipients=["oniyonkuru233@gmail.com"],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )
    
    try:
        mail.send(msg)
        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        print("Email error:", e)
        flash("Failed to send message. Please try again later.", "danger")

    return redirect(request.referrer)

# ==========================================
# Forgot-password Routes
# ==========================================

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            token = serializer.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)

            # Send email
            msg = Message("Reset Your Password", recipients=[user.email])
            msg.html = f"""
            <p>Hello {user.full_name},</p>
            <p>You requested a password reset. Click the link below to reset your password:</p>
            <p><a href="{reset_url}" style="background:#00a859;color:white;padding:10px 16px;border-radius:6px;text-decoration:none;">Reset Password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            """
            mail.send(msg)

            flash('A password reset link has been sent to your email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found. Please use a registered email.', 'danger')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

# ==========================================
# Reset-password Routes
# ==========================================

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=1800)  # 30 min
    except:
        flash('The reset link is invalid or expired.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(request.url)
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return redirect(request.url)

        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        flash('Password has been reset successfully! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')



# ==========================================
# Authentication Routes
# ==========================================
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        national_id = request.form['national_id']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        if User.query.filter((User.email == email) | (User.national_id == national_id)).first():
            flash('Email or National ID already registered.', 'warning')
            return redirect(url_for('register'))

        new_user = User(full_name=full_name, national_id=national_id, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('thank_you', role=role))

    return render_template('register.html')


@app.route('/auth/thank-you')
def thank_you():
    role = request.args.get('role')
    return render_template('thank-you.html', role=role)


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if admin first
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Otherwise, check user
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('employee_dashboard') if user.role == 'EMPLOYEE' else url_for('employer_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/auth/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))




# ==========================================
# Employee Routes
# ==========================================
@app.route('/employee/dashboard')
@employee_required
def employee_dashboard():
    user_id = session['user_id']
    applications = Application.query.filter_by(user_id=user_id).join(Job).order_by(Application.applied_at.desc()).all()
    announcements = get_announcements()
    return render_template('employee/dashboard.html', applications=applications, announcements=announcements)

@app.route('/employee/profile', methods=['GET', 'POST'])
@employee_required
def employee_profile():
    user_id = session['user_id']
    profile = EmployeeProfile.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        phone = request.form.get('phone')
        location = request.form.get('location')
        education = request.form.get('education')
        skills = request.form.get('skills')
        experience = request.form.get('experience')

        if profile:
            profile.phone = phone
            profile.location = location
            profile.education = education
            profile.skills = skills
            profile.experience = experience
        else:
            profile = EmployeeProfile(user_id=user_id, phone=phone, location=location,
                                      education=education, skills=skills, experience=experience)
            db.session.add(profile)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employee_profile'))

    return render_template('employee/profile.html', profile=profile)



@app.route('/jobs')
@employee_required
def browse_jobs():
    q = request.args.get('q')
    location = request.args.get('location')
    jtype = request.args.get('type')
    query = Job.query.join(Company)
    if q: query = query.filter(Job.title.ilike(f"%{q}%"))
    if location: query = query.filter(Job.location == location)
    if jtype: query = query.filter(Job.type == jtype)
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template('employee/jobs.html', jobs=jobs)

@app.route('/jobs/<int:job_id>/apply', methods=['GET', 'POST'])
@employee_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    user_id = session['user_id']

    if request.method == 'POST':
        cover_letter_file = request.files.get('cover_letter')

        # Validate file
        if not cover_letter_file or cover_letter_file.filename == '':
            flash('Please upload a cover letter document.', 'warning')
            return redirect(request.url)

        if not allowed_file(cover_letter_file.filename):
            flash('Invalid file type. Please upload a PDF, DOC, or DOCX.', 'danger')
            return redirect(request.url)

        # Prevent duplicate applications
        if Application.query.filter_by(user_id=user_id, job_id=job_id).first():
            flash('You have already applied for this job.', 'warning')
            return redirect(url_for('browse_jobs'))

        # Save file
        filename = secure_filename(cover_letter_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cover_letter_file.save(filepath)

        # Save ONLY the filename in the database
        application = Application(
            user_id=user_id,
            job_id=job_id,
            cover_letter=filename  # <--- FIX: store only filename
        )
        db.session.add(application)
        db.session.commit()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('employee_dashboard'))

    return render_template('employee/apply.html', job=job)


# ==========================================
# Upload Employee Documents
# ==========================================
@app.route('/employee/documents', methods=['GET', 'POST'], endpoint='upload_documents')
@employee_required
def upload_documents():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    # Allowed file types
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        if 'document' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['document']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save file to static/uploads
            filename = secure_filename(file.filename)
            upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Save record in EmployeeDocument table
            file_type = request.form.get('file_type', 'CV')  # default type if not provided
            doc = EmployeeDocument(
                user_id=user_id,
                file_name=filename,
                file_path=filepath,
                file_type=file_type
            )
            db.session.add(doc)
            db.session.commit()

            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('upload_documents'))
        else:
            flash('Invalid file type. Allowed types: pdf, doc, docx', 'danger')
            return redirect(request.url)

    # GET request: show uploaded documents
    documents = EmployeeDocument.query.filter_by(user_id=user_id).all()
    return render_template('employee/documents.html', documents=documents, user=user)




# (Other Employee Routes remain unchanged)
# ==========================================
# Employer Routes
# ==========================================
# ==========================================
# Employer Routes
# ==========================================
@app.route('/employer')
@employer_required
def employer_dashboard():
    owner_id = session['user_id']
    company = Company.query.filter_by(owner_id=owner_id).first()
    jobs = Job.query.join(Company).filter(Company.owner_id == owner_id).order_by(Job.created_at.desc()).all()

    total_jobs = len(jobs)
    job_ids = [j.id for j in jobs]
    total_applications = Application.query.filter(Application.job_id.in_(job_ids)).count() if job_ids else 0
    recent_applications = (
        Application.query.join(Job)
        .filter(Job.id.in_(job_ids))
        .order_by(Application.applied_at.desc())
        .limit(5)
        .all()
        if job_ids else []
    )
    announcements = get_announcements()

    return render_template(
        'employer/dashboard.html',
        company=company,
        jobs=jobs,
        total_jobs=total_jobs,
        total_applications=total_applications,
        recent_applications=recent_applications,
        announcements=announcements
    )


@app.route('/employer/company', methods=['GET', 'POST'])
@employer_required
def company_profile():
    owner_id = session['user_id']
    company = Company.query.filter_by(owner_id=owner_id).first()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        website = request.form.get('website')

        if company:
            company.name = name
            company.description = description
            company.website = website
            db.session.commit()
            flash('Company profile updated.', 'success')
        else:
            new_company = Company(name=name, description=description, website=website, owner_id=owner_id)
            db.session.add(new_company)
            db.session.commit()
            flash('Company profile created.', 'success')

        return redirect(url_for('employer_dashboard'))

    return render_template('employer/company_profile.html', company=company)


@app.route('/employer/jobs/create', methods=['GET', 'POST'])
@employer_required
def create_job():
    owner_id = session['user_id']
    company = Company.query.filter_by(owner_id=owner_id).first()
    if not company:
        flash('Please create your company profile first.', 'warning')
        return redirect(url_for('company_profile'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        salary = request.form.get('salary')
        jtype = request.form.get('type')
        deadline = request.form.get('deadline')

        job = Job(
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            salary=salary,
            type=jtype or 'FULL_TIME',
            deadline=datetime.fromisoformat(deadline) if deadline else None,
            company_id=company.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully.', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('employer/job_form.html', job=None)


@app.route('/employer/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
@employer_required
def edit_job(job_id):
    owner_id = session['user_id']
    job = Job.query.get_or_404(job_id)
    if job.company.owner_id != owner_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('employer_dashboard'))

    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.requirements = request.form.get('requirements')
        job.location = request.form.get('location')
        job.salary = request.form.get('salary')
        job.type = request.form.get('type')
        deadline = request.form.get('deadline')
        job.deadline = datetime.fromisoformat(deadline) if deadline else None

        db.session.commit()
        flash('Job updated successfully.', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('employer/job_form.html', job=job)


@app.route('/employer/jobs/<int:job_id>/delete', methods=['POST'])
@employer_required
def delete_job(job_id):
    owner_id = session['user_id']
    job = Job.query.get_or_404(job_id)
    if job.company.owner_id != owner_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('employer_dashboard'))

    db.session.delete(job)
    db.session.commit()
    flash('Job deleted.', 'info')
    return redirect(url_for('employer_dashboard'))


@app.route('/employer/jobs/<int:job_id>/applicants')
@employer_required
def view_applicants(job_id):
    owner_id = session['user_id']
    job = Job.query.get_or_404(job_id)
    if job.company.owner_id != owner_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('employer_dashboard'))

    applicants = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    return render_template('employer/applicants.html', job=job, applicants=applicants)

@app.route('/employer/applicants/<int:app_id>')
@employer_required
def view_applicant_detail(app_id):
    """View full applicant profile and uploaded documents"""
    owner_id = session['user_id']
    application = Application.query.get_or_404(app_id)
    job = application.job

    # Security: ensure employer owns this job
    if job.company.owner_id != owner_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('employer_dashboard'))

    applicant = application.user
    profile = EmployeeProfile.query.filter_by(user_id=applicant.id).first()
    documents = EmployeeDocument.query.filter_by(user_id=applicant.id).all()

    return render_template(
        'employer/applicant_detail.html',
        applicant=applicant,
        profile=profile,
        documents=documents,
        job=job,
        application=application
    )



@app.route('/employer/applications/<int:app_id>/status', methods=['POST'])
@employer_required
def update_application_status(app_id):
    owner_id = session['user_id']
    application = Application.query.get_or_404(app_id)
    if application.job.company.owner_id != owner_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('employer_dashboard'))

    new_status = request.form.get('status')
    if new_status not in ['APPLIED', 'SHORTLISTED', 'REJECTED', 'HIRED']:
        flash('Invalid status', 'danger')
    else:
        application.status = new_status
        db.session.commit()
        flash('Application status updated.', 'success')

    return redirect(url_for('view_applicants', job_id=application.job.id))
# ==========================================
# Admin Routes
# ==========================================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    total_announcements = Announcement.query.count()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_jobs=total_jobs,
        total_applications=total_applications,
        total_announcements=total_announcements
    )


@app.route('/admin/users', endpoint='manage_users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/jobs', endpoint='manage_jobs')
@admin_required
def manage_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/jobs.html', jobs=jobs)


@app.route('/admin/applications', endpoint='manage_applications')
@admin_required
def manage_applications():
    applications = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template('admin/applications.html', applications=applications)


@app.route('/admin/announcements', methods=['GET', 'POST'], endpoint='manage_announcements')
@admin_required
def manage_announcements():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        ann = Announcement(title=title, content=content)
        db.session.add(ann)
        db.session.commit()
        flash('Announcement published!', 'success')
        return redirect(url_for('manage_announcements'))

    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements)


@app.route('/admin/announcements/<int:ann_id>/delete', endpoint='delete_announcement')
@admin_required
def delete_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    db.session.delete(ann)
    db.session.commit()
    flash('Announcement deleted.', 'info')
    return redirect(url_for('manage_announcements'))


@app.route('/admin/new', methods=['GET', 'POST'], endpoint='add_admin')
@admin_required
def add_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if Admin.query.filter_by(email=email).first():
            flash('Admin already exists.', 'warning')
        else:
            admin = Admin(email=email)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            flash('New admin added successfully.', 'success')
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/new_admin.html')


@app.route('/admin/users/<int:user_id>/block', endpoint='block_user')
@admin_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.full_name} removed from system.', 'info')
    return redirect(url_for('manage_users'))


# =========================
# Admin: Delete Job
# =========================
@app.route('/admin/jobs/<int:job_id>/delete', endpoint='delete_job_admin')
@admin_required
def delete_job_admin(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash(f'Job "{job.title}" removed by admin.', 'info')
    return redirect(url_for('manage_jobs'))





# (Other admin routes remain unchanged: manage users, jobs, announcements, add admin)
# ==========================================
# Run App
# ==========================================
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=10000)
