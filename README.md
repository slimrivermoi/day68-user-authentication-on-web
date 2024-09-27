# Udemy day 68: User Authentication on Web
The goal of this project is to set up a secured user authentication on the web using Level 4 password encryption techniques (i.e. hashing and salting), Flask login_manager. 

**Registration page**: the user can enter name, email address and password.
- If the email address does not exist, the user account will then be generated and stored in the database.
- The password will then been "hash and salted" (Level 4 authentication) before being stored in the DB.
- The logged in user will be directed to "Secret Page" to download a document.  

**Login page**: the user enters email address and password.
- If the email and password matched, user will be directed to "Secret Page" to download a document.  


|  | Description |
| ----------- | ----------- |
| Languages | Python, html, css |
| Python Libraries | Flask, SQLAlchemy, flask_login, werkzeug.security |



How to run the file:
-
- Clone the repo and execute main.py.
- On your browser, copy and paste: http://127.0.0.1:5003.


**Demo Video**

https://github.com/user-attachments/assets/32170f93-023e-431d-a851-c092e8940184


