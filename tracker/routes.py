from tracker import app, db
from tracker.models import User, Expense, Category
from flask import render_template, redirect, url_for, flash, request
from tracker.forms import RegisterForm, LoginForm, ExpenseForm, CategoryForm, DeleteExpenseForm
from flask_login import login_user, logout_user, login_required, current_user

from tracker import app

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
@login_required
def home_page():
    expense_form = ExpenseForm()
    category_form = CategoryForm()
    delete_expense_form = DeleteExpenseForm()

    if "submit_expense" in request.form and expense_form.validate_on_submit():
        expense_to_create = Expense(name=expense_form.name.data,
                                    category=expense_form.category.data,
                                    amount=expense_form.amount.data,
                                    user_id=current_user.user_id)
        db.session.add(expense_to_create)
        db.session.commit()
        flash(f'Expense "{expense_to_create.name}" added successfully!', category='success')
        return redirect(url_for('home_page'))

    if expense_form.errors != {}:
        for err_msg in expense_form.errors.values():
            flash(err_msg[0], category="danger")

    if "submit_category" in request.form and category_form.validate_on_submit():
        category_to_create = Category(name=category_form.name.data, user_id=current_user.user_id)
        db.session.add(category_to_create)
        db.session.commit()
        flash(f'Category "{category_to_create.name}" added successfully!', category='success')
        return redirect(url_for('home_page'))

    if category_form.errors != {}:
        for err_msg in category_form.errors.values():
            flash(err_msg[0], category="danger")

    if "delete_expense" in request.form and delete_expense_form.validate_on_submit():
        expense_to_delete = Expense.query.filter_by(expense_id=request.form.get("deleted_expense")).first()
        if expense_to_delete:
            db.session.delete(expense_to_delete)
            db.session.commit()
            flash(f'Expense "{expense_to_delete.name}" deleted successfully!', category='info')
            return redirect(url_for('home_page'))
        else:
            flash(f'Expense not found!', category='danger')

    if delete_expense_form.errors != {}:
        for err_msg in delete_expense_form.errors.values():
            flash(err_msg[0], category="danger")

    expenses = Expense.query.filter_by(user_id=current_user.user_id)
    return render_template('home.html', expenses=expenses, expense_form=expense_form, category_form=category_form, delete_expense_form=delete_expense_form)

@app.route('/statistics', methods=["GET", "POST"])
@login_required
def statistics_page():
    return render_template('statistics.html')

@app.route('/register', methods=["GET", "POST"])
def register_page():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        user_to_create = User(username=register_form.username.data,
                              email_address=register_form.email_address.data,
                              password=register_form.password1.data)

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('home_page'))

    if register_form.errors != {}:
        for err_msg in register_form.errors.values():
            flash(f'There was an error with creating the user: {err_msg}', category="danger")

    return render_template('register.html', register_form=register_form)

@app.route('/login', methods=["GET", "POST"])
def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if not attempted_user:
            flash("Username does not exist!", category="danger")
            return redirect(url_for('login_page'))
        if not attempted_user.check_password_correction(attempted_password=login_form.password.data):
            flash("Incorrect password!", category="danger")
            return redirect(url_for('login_page'))

        login_user(attempted_user)
        return redirect(url_for('home_page'))

    return render_template('login.html', login_form=login_form)

@app.route('/logout', methods=["GET", "POST"])
def logout_page():
    logout_user()
    flash("You have been successfully logged out!", category="info")
    return redirect(url_for('login_page'))