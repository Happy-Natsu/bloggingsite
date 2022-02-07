from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User





class RegistrationForm(FlaskForm):
	username = StringField('username', 
		validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('password',
		validators=[DataRequired()])
	confirm_password = PasswordField('confirm password',
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That user name is taken. Please choose different one!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose different one!')


class LoginForm(FlaskForm):
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('password',
		validators=[DataRequired()])
	remember = BooleanField('Remembr Me')
	submit = SubmitField('log in')

class UpdateAccountForm(FlaskForm):
	username = StringField('username', 
		validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That user name is taken. Please choose different one!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose different one!')


class RequestResetForm(FlaskForm):
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('Ther is no account with that email. You must reguster first.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('password',
		validators=[DataRequired()])
	confirm_password = PasswordField('confirm password',
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')