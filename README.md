JobConnect Rwanda — Job Recruitment Platform

JobConnect Rwanda is a web-based job recruitment system built with Flask, designed to connect job seekers and employers in Rwanda.
The platform enables employers to post job listings, review applications, and manage recruitment efficiently, while job seekers can search for opportunities, apply with uploaded cover letters, and track their application status.

Features
Job Seeker (Employee)

Register and log in securely

Browse and search for job listings

View full job descriptions (Title, Description, Requirements, and Salary)

Apply for jobs with uploaded cover letters (PDF/DOC/DOCX)

Manage and track submitted applications

Reset forgotten passwords via email verification

Employer

Register and manage company profile

Post, edit, and delete job listings

View applicants for each job

View and download uploaded cover letters

Shortlist, reject, or hire applicants

Logout functionality for session security

Administrator

Secure login for admins

Manage users, jobs, and announcements

View total counts of users, jobs, applications, and announcements

Add new administrators

Delete or block users

Publish and manage announcements for employers and job seekers

View all job applications in one place

Installation & Setup

1. Clone the repository:
   git clone https://github.com/Niyonkuru-olivier/job_connect_rwanda.git

2. Navigate to the project directory:
   cd HireMeRwanda

3. Install dependencies:
   pip install -r requirements.txt

4. Set up your MySQL database and update the configuration in app.py.

5. Run database migrations if necessary.

6. Start the Flask application:
   flask run

7. Access the system via: http://127.0.0.1:5000
