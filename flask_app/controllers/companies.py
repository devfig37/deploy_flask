import requests
import os
from flask_app.models.company import Company
from flask_app.models.user import User
from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.one_user(data)
    print(user)
    return render_template('dashboard.html', companies=Company.get_all_companies_with_users(), user=User.one_user(data))


@app.route('/api_call', methods=['GET'])
def api_call():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
    r = requests.get(url)
    data = r.json()
    print(data)
    return render_template('api_call.html', data=data['Time Series (5min)'], company=data['Meta Data'])


@app.route('/api')
def api():
    return redirect('/api_call')


@ app.route('/new')
def new_company():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.one_user(data)
    print(user)
    return render_template('new_company.html', companies=Company.get_all_companies_with_users(), user=User.one_user(data))


@ app.route('/create', methods=['POST'])
def create_company():
    if 'user_id' not in session:
        return redirect('/')
    valid = Company.validate_company(request.form)
    if valid:
        data = {
            'name': request.form['name'],
            'amount': request.form['amount'],
            'paid': request.form['paid'],
            'users_id': session['user_id']

        }
        company = Company.create_company(data)
        return redirect('/add_company')
    return redirect('/add_company')


@ app.route('/add_company')
def add_company_form():
    return redirect('/dashboard')


@ app.route('/all_companies')
def all_companies():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.one_user(data)
    print(user)
    return render_template('all_companies.html', companies=Company.get_all_companies_with_users(), user=user)


@ app.route('/<int:company_id>/edit')
def edit(company_id):
    data = {
        'id': company_id
    }
    return render_template('edit_company.html', company=Company.get_one(data))


@ app.route('/<int:company_id>/update', methods=['POST'])
def update_company(company_id):
    Company.update_company(request.form)
    return redirect('/dashboard')


@ app.route('/<int:company_id>/delete')
def destroy(company_id):
    data = {
        'id': company_id
    }
    Company.destroy(data)
    return redirect('/dashboard')


@ app.route('/<int:company_id>')
def company_page(company_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.one_user(user_data)
    data = {
        'id': company_id
    }
    return render_template('one_company.html', company=Company.get_one(data), user=user)
