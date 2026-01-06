from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo, Regexp, ValidationError
from flask_ckeditor import CKEditorField
import re


# Custom validator for password strength
def password_strength(form, field):
    password = field.data
    errors = []
    if not re.search(r'[A-Z]', password):
        errors.append('at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        errors.append('at least one lowercase letter')
    if not re.search(r'\d', password):
        errors.append('at least one number')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('at least one special character (!@#$%^&*(),.?":{}|<>)')
    if errors:
        raise ValidationError(f'Password must contain {", ".join(errors)}.')


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# WTForm for registering new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address."),
        Length(max=120, message="Email must be less than 120 characters.")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required."),
        Length(min=8, max=128, message="Password must be between 8 and 128 characters."),
        password_strength
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters."),
        Regexp(r'^[a-zA-Z\s\-\']+$', message="Name can only contain letters, spaces, hyphens, and apostrophes.")
    ])
    submit = SubmitField("Sign Me Up!")


# WTForm for logging in existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# WTForm for users to leave comments below posts
class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")


# WTForm for contact page
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required."),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Email is required."),
        Email(message="Please enter a valid email address.")
    ])
    phone = StringField("Phone", validators=[
        Length(max=20, message="Phone number must be less than 20 characters.")
    ])
    message = TextAreaField("Message", validators=[
        DataRequired(message="Message is required."),
        Length(min=10, max=2000, message="Message must be between 10 and 2000 characters.")
    ])
    submit = SubmitField("Send")
