from __future__ import unicode_literals

from django.db import models

import datetime
from dateutil.parser import *

import re, bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')
password_regex = re.compile(r'^[.]{8,}$')


# Create your models here.

class userManager(models.Manager):
    def registration_validator(self, submitted_data):

        errors = []
        flag = False
        users = User.objects.all()
        today = datetime.datetime.now()
        entered_dob = submitted_data["dob"].encode()

        try:
            dob = parse(str(submitted_data["dob"]))
            if dob.date() > today.date():
                errors.append("You cannot be born after today!")
                flag = False
        except:
            errors.append("Date of birth cannot be empty!")
            flag = False

        if len(submitted_data["first_name"]) < 2:
            errors.append("First name must contain no fewer than 2 characters.")
            flag = True
        if not name_regex.match(submitted_data["first_name"]):
            errors.append("First name can contain only letters.")
            flag = True

        if len(submitted_data["last_name"]) < 2:
            errors.append("Last name must contain no fewer than 2 characters.")
            flag = True
        if not name_regex.match(submitted_data["last_name"]):
            errors.append("Last name must contain only letters.")
            flag = True

        for user in users:
            if submitted_data["alias"] == user.alias:
                errors.append("Alias already exists in database! Please choose a different moniker!")
                flag = True

        for user in users:
            if submitted_data["email"] == user.email:
                errors.append("Email already exists in database! Please use a different email!")
                flag = True
        if not email_regex.match(submitted_data["email"]):
            errors.append("Please enter a valid email.")
            flag = True

        if len(submitted_data["password"]) < 8:
            errors.append("Password must contain at least 8 characters.")
            flag = True
        if not submitted_data["password"] == submitted_data["confirm_password"]:
            errors.append("Please make sure that your confirmation password matches your password exactly.")
            flag = True

        if not flag:
            hashed_password = bcrypt.hashpw(submitted_data["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(
                first_name = submitted_data["first_name"],
                last_name = submitted_data["last_name"],
                alias = submitted_data["alias"],
                email = submitted_data["email"],
                password = hashed_password,
                dob = submitted_data["dob"]
                )
            return (flag, user)
        return (flag, errors)

    def login_validator(self, submitted_data):
        try:
            user = User.objects.get(email = submitted_data["email"])
            entered_password = submitted_data["password"].encode()
            hashed_password = user.password.encode()
            if bcrypt.hashpw(entered_password, hashed_password) == user.password:
                return (True, user)
            else:
                return (False, "Login credentials incorrect")
        except:
            return (False, "Login credentials incorrect")

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    alias = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    dob = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = userManager()
