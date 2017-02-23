from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, postData):
        errors = []
        modelResponse = {}
        user = Users.objects.filter(email=postData["email"])
        if len(user) < 1:
            errors.append("That email doesn't exist")
        else:
            if bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
                modelResponse["loggedin"] = True
                modelResponse["user"] = user[0]
            else:
                errors.append("Password is incorrect")
        if errors:
            modelResponse["loggedin"] = False
            errors.append("Please try logging in again")
            modelResponse["errors"] = errors
        return modelResponse

    def register(self, postData):
        noErrors = True
        errors = []
        modelResponse = {}
        if len(postData["first_name"]) < 2:
            errors.append("First name needs to be greater than 2 letters.")
            noErrors = False
        if len(postData["last_name"]) < 2:
            errors.append("Last name needs to be greater than 2 letters.")
            noErrors = False
        if len(postData["password"]) < 2:
            errors.append("Password needs to be greater than 2 letters.")
            noErrors = False
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Not a validito email address.")
            noErrors = False
        if len(postData["password"]) < 8:
            errors.append("Password needs to be at least 8 characters long")
            noErrors = False
        if postData["password"] != postData["confirm-pw"]:
            errors.append("Passwords don't match.")
            noErrors = False
        if noErrors:
            modelResponse["registered"] = True
            pw_hash = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            modelResponse["user"] = Users.objects.create(first_name=postData["first_name"], last_name=postData["last_name"],email=postData["email"],password=pw_hash)
        else:
            modelResponse["registered"] = False
            errors.append("Please try registering again")
            modelResponse["errors"] = errors
        return modelResponse

class Users(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  objects = UserManager()
