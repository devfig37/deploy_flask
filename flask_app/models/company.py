from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Company():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.paid = data['paid']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.creator = None
        self.users_who_voted = []

    @classmethod
    def get_all_companies(cls):
        query = "SELECT * FROM personal_project.companies;"
        return connectToMySQL('personal_project').query_db(query)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM personal_project.companies WHERE id = %(id)s;"
        results = connectToMySQL('personal_project').query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_company(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        query = "SELECT * FROM companies WHERE name = %(name)s"
        results = connectToMySQL('personal_project').query_db(query, data)
        if len(results) != 0:
            flash('Company exists!')
            is_valid = False
        if len(data['amount']) < 1:
            flash("Amount must be at least 1 character.")
            is_valid = False
        if len(data['paid']) < 2:
            flash("Paid must be at least 2 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def create_company(cls, data):
        query = "INSERT INTO companies (name, amount, paid, users_id, created_at, updated_at) VALUES (%(name)s, %(amount)s, %(paid)s, %(users_id)s, NOW(), NOW())"
        return connectToMySQL('personal_project').query_db(query, data)

    @classmethod
    def get_all_companies_with_users(cls):
        query = "SELECT * FROM companies LEFT JOIN users ON companies.users_id = users.id;"
        companies = connectToMySQL('personal_project').query_db(query)
        results = []
        for company in companies:
            data = {
                'id': company['id'],
                'first_name': company['first_name'],
                'last_name': company['last_name'],
                'email': company['email'],
                'password': company['password'],
                'created_at': company['users.created_at'],
                'updated_at': company['users.updated_at']
            }
            one_company = cls(company)
            one_company.creator = user.User(data)
            results.append(one_company)
        return results

    @classmethod
    def get_all_companies_with_users_votes(cls):
        query = "Select * from companies left join users on users.id = companies.users_id left join votes on companies.id = votes.companies_id left join users as users2 on votes.users_id = users2.id order by companies.created_at desc;"
        companies = connectToMySQL('personal_project').query_db(query)
        results = []
        for company in companies:
            new_company = True
            data = {
                'id': company['users2.id'],
                'first_name': company['users2.first_name'],
                'last_name': company['users2.last_name'],
                'email': company['users2.email'],
                'password': company['users2.password'],
                'created_at': company['users2.created_at'],
                'updated_at': company['users2.updated_at']
            }

            if len(results) > 0 and results[len(results) - 1].id == results['id']:
                results[len(results) -
                        1].users_who_voted.append(user.User(data))
                new_company = False
            if new_company:
                ncompany = cls(pie)
                data = {
                    'id': company['users.id'],
                    'first_name': company['first_name'],
                    'last_name': company['last_name'],
                    'email': company['email'],
                    'password': company['password'],
                    'created_at': company['users.created_at'],
                    'updated_at': company['users.updated_at']
                }
                ncompany.creator = user.User(data)
                if company['users2.id'] is not None:
                    ncompany.users_who_voted.append(user.User(data))
                results.append(pie)
        return results

    @classmethod
    def update_company(cls, data):
        query = "UPDATE companies SET name=%(name)s, amount=%(amount)s, paid=%(paid)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL('personal_project').query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM companies WHERE id=%(id)s"
        return connectToMySQL('personal_project').query_db(query, data)
