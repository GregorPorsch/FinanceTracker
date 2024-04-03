from tracker import app, db
from tracker.models import User, Transaction, Category
from flask import render_template, redirect, url_for, flash, request, jsonify
from tracker.forms import RegisterForm, LoginForm, TransactionForm, CategoryForm, DeleteTransactionForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, and_
from datetime import datetime, timedelta

from tracker import app

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
@login_required
def home_page():
    transaction_form = TransactionForm()
    category_form = CategoryForm()
    delete_transaction_form = DeleteTransactionForm()

    if "submit_transaction" in request.form and transaction_form.validate_on_submit():
        transaction_to_create = Transaction(name=transaction_form.name.data,
                                    type=transaction_form.type.data,
                                    category=transaction_form.category.data,
                                    amount=transaction_form.amount.data,
                                    user_id=current_user.user_id)
        db.session.add(transaction_to_create)

        if transaction_form.type.data == "Expense":
            current_user.expenses += float(transaction_form.amount.data)
        else:
            current_user.income += float(transaction_form.amount.data)

        db.session.commit()
        flash(f'Transaction "{transaction_to_create.name}" added successfully!', category='success')
        return redirect(url_for('home_page'))

    if transaction_form.errors != {}:
        for err_msg in transaction_form.errors.values():
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

    if "delete_transaction" in request.form and delete_transaction_form.validate_on_submit():
        transaction_to_delete = Transaction.query.filter_by(transaction_id=request.form.get("deleted_transaction")).first()
        if transaction_to_delete:
            db.session.delete(transaction_to_delete)
            db.session.commit()
            flash(f'Transaction "{transaction_to_delete.name}" deleted successfully!', category='info')
            return redirect(url_for('home_page'))
        else:
            flash(f'Transaction not found!', category='danger')

    if delete_transaction_form.errors != {}:
        for err_msg in delete_transaction_form.errors.values():
            flash(err_msg[0], category="danger")

    transactions = Transaction.query.filter_by(user_id=current_user.user_id)
    return render_template('home.html', transactions=transactions, transaction_form=transaction_form, category_form=category_form, delete_transaction_form=delete_transaction_form)

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

@app.route('/api/expenses_by_category', methods=["GET"])
@login_required
def expenses_by_category():
    expenses = Transaction.query.filter_by(user_id=current_user.user_id, type="Expense").all()
    return jsonify([{"amount": expense.amount_rounded, "category": expense.category} for expense in expenses])

@app.route('/api/incomes_by_category', methods=["GET"])
@login_required
def incomes_by_category():
    incomes = Transaction.query.filter_by(user_id=current_user.user_id, type="Income").all()
    return jsonify([{"amount": income.amount_rounded, "category": income.category} for income in incomes])


@app.route('/api/transactions_over_time', methods=["GET"])
@login_required
def transactions_over_time():
    time_period = request.args.get('time_period', default='month', type=str)

    if time_period == 'month':
        start_date = datetime.now() - timedelta(days=30)
    elif time_period == 'week':
        start_date = datetime.now() - timedelta(weeks=1)
    else:
        start_date = datetime.now() - timedelta(days=1)

    transactions = db.session.query(
        func.date(Transaction.date).label('date'),
        func.sum(Transaction.amount_rounded).label('total'),
        Transaction.type
    ).filter(
        and_(
            Transaction.user_id == current_user.user_id,
            Transaction.date >= start_date
        )
    ).group_by(
        'date',
        Transaction.type
    ).all()

    # Initialize data for all dates within the selected time period
    data = {}
    current_date = start_date
    while current_date <= datetime.now():
        date_str = current_date.strftime('%Y-%m-%d')
        data[date_str] = {'income': 0, 'expense': 0}
        current_date += timedelta(days=1)

    # Update data with actual transaction totals
    for transaction in transactions:
        transaction_date_object = datetime.strptime(transaction.date, '%Y-%m-%d')
        date = transaction_date_object.strftime('%Y-%m-%d')
        if transaction.type == 'Income':
            data[date]['income'] = transaction.total
        else:
            data[date]['expense'] = transaction.total

    return jsonify(data)