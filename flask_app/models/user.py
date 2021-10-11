from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import Flask, app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM personal_project.users;"
        results = connectToMySQL('personal_project').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def one_user(cls, data):
        query = "SELECT * FROM personal_project.users WHERE id=%(id)s;"
        results = connectToMySQL('personal_project').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO personal_project.users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(hashed_password)s );"
        return connectToMySQL('personal_project').query_db(query, data)

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('personal_project').query_db(query, data)
        if len(results) != 0:
            flash('Email exists! Please login.')
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords must match!')
            is_valid = False
        return is_valid

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM personal_project.users WHERE email = %(email)s;"
        results = connectToMySQL('personal_project').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM personal_project.users WHERE id=%(id)s;"
        return connectToMySQL('personal_project').query_db(query, data)
