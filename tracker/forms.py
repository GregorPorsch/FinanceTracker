from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DecimalField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

from tracker.models import Category
from tracker.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        username = User.query.filter_by(username=username_to_check.data).first()
        if username:
            raise ValidationError("Username already exists. Please choose a different username.")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("E-Mail Address already exists. Please choose a different E-Mail Address.")

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class ExpenseForm(FlaskForm):
    def validate_amount(self, amount_to_check):
        if not amount_to_check.data or amount_to_check.data <= 0:
            raise ValidationError("Please enter a positive amount!")

    name = StringField(label="Name", validators=[Length(min=1, max=30), DataRequired()])
    category = SelectField(label="Category", validators=[DataRequired()])
    amount = DecimalField(label="Amount", validators=[DataRequired()], places=2, default=0.0)
    submit = SubmitField(label="Submit expense", name="submit_expense")

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        categories = Category.query.filter_by(user_id=current_user.user_id).all()
        if categories:
            self.category.choices = [(category.name, category.name) for category in categories]
        else:
            self.category.choices = [('No categories yet', 'No categories yet')]
            self.category.render_kw = {'disabled': 'disabled'}

class CategoryForm(FlaskForm):
    def validate_name(self, name_to_check):
        category = Category.query.filter_by(name=name_to_check.data, user_id=current_user.user_id).first()
        if category:
            raise ValidationError("Category already exists. Please choose a different category name.")

    name = StringField(label="Category Name", validators=[Length(min=1, max=30), DataRequired()])
    submit = SubmitField(label="Add category", name="submit_category")

class DeleteExpenseForm(FlaskForm):
    submit = SubmitField(label="Delete", name="delete_expense")
