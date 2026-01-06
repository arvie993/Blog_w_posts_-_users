from datetime import date
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import Flask, abort, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

load_dotenv()
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, ContactForm


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


# Custom Gravatar function for Flask 3.x compatibility
def gravatar_url(email, size=100, default='retro', rating='g'):
    """Generate Gravatar URL for an email address."""
    hash_value = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_value}?s={size}&d={default}&r={rating}"


# Register gravatar function as a Jinja2 filter
app.jinja_env.filters['gravatar'] = gravatar_url

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///posts.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Parent relationship to Comment: "parent_post" refers to the parent_post property in Comment
    comments = relationship("Comment", back_populates="parent_post")


# User table for registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    # Parent relationship to Comment: "comment_author" refers to the comment_author property in Comment
    comments = relationship("Comment", back_populates="comment_author")


# Comment table for blog post comments
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship to User: "comments" refers to the comments property in User
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child relationship to BlogPost: "comments" refers to the comments property in BlogPost
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


with app.app_context():
    db.create_all()


# Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user email already exists
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        
        # Hash and salt the password
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        # Log in and authenticate user after adding details to database
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


# Retrieve a user from the database based on their email.
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # Find user by email
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    # Only allow logged-in users to comment
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "error": "You need to login or register to comment."}), 401
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        
        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "success": True, 
                "message": "Comment added successfully!",
                "comment": {
                    "id": new_comment.id,
                    "text": new_comment.text,
                    "author_name": current_user.name,
                    "author_email": current_user.email,
                    "gravatar": gravatar_url(current_user.email),
                    "can_delete": True
                }
            })
    return render_template("post.html", post=requested_post, form=comment_form)


# Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "success": True, 
                "message": "Post created successfully!",
                "redirect": url_for("get_all_posts")
            })
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                "success": True, 
                "message": "Post updated successfully!",
                "redirect": url_for("show_post", post_id=post.id)
            })
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, post_id=post_id)


# Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Allow comment author or admin to delete a comment
@app.route("/delete-comment/<int:comment_id>", methods=["DELETE", "GET"])
def delete_comment(comment_id):
    comment_to_delete = db.get_or_404(Comment, comment_id)
    post_id = comment_to_delete.post_id
    # Check if current user is the comment author or admin
    if not current_user.is_authenticated:
        if request.method == "DELETE":
            return jsonify({"success": False, "error": "You need to be logged in to delete comments."}), 401
        flash("You need to be logged in to delete comments.")
        return redirect(url_for('login'))
    if current_user.id != comment_to_delete.author_id and current_user.id != 1:
        if request.method == "DELETE":
            return jsonify({"success": False, "error": "You can only delete your own comments."}), 403
        flash("You can only delete your own comments.")
        return redirect(url_for('show_post', post_id=post_id))
    db.session.delete(comment_to_delete)
    db.session.commit()
    if request.method == "DELETE":
        return jsonify({"success": True, "message": "Comment deleted successfully."})
    return redirect(url_for('show_post', post_id=post_id))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    msg_sent = False
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data
        
        # Get admin user (id=1) email from database
        admin_user = db.session.execute(db.select(User).where(User.id == 1)).scalar()
        
        if admin_user:
            admin_email = admin_user.email
            
            # Try to send email
            try:
                mail_server = os.environ.get('MAIL_SERVER')
                mail_port = int(os.environ.get('MAIL_PORT', 587))
                mail_username = os.environ.get('MAIL_USERNAME')
                mail_password = os.environ.get('MAIL_PASSWORD')
                
                if mail_username and mail_password:
                    # Create email message
                    msg = MIMEMultipart()
                    msg['From'] = mail_username
                    msg['To'] = admin_email
                    msg['Subject'] = f"New Contact Form Message from {name}"
                    
                    body = f"""You have received a new message from your blog contact form:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}

Message:
{message}

---
This message was sent from Aravind's Blog contact form.
"""
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Send email
                    with smtplib.SMTP(mail_server, mail_port) as server:
                        server.starttls()
                        server.login(mail_username, mail_password)
                        server.sendmail(mail_username, admin_email, msg.as_string())
                    
                    print(f"Email sent to admin ({admin_email}) from {name} ({email})")
                else:
                    print(f"Email config not set. Contact form submitted: {name}, {email}, {phone}, {message}")
            except Exception as e:
                print(f"Failed to send email: {e}")
                print(f"Contact form submitted: {name}, {email}, {phone}, {message}")
        else:
            print(f"No admin user found. Contact form submitted: {name}, {email}, {phone}, {message}")
        
        msg_sent = True
    return render_template("contact.html", form=form, msg_sent=msg_sent)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
