from __future__ import unicode_literals

from django.db import models

import md5
import bcrypt
import os, binascii

import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def login(self, postData):
        messages = []
        email = postData['email']
        password = postData['password']
        if len(str(email)) < 1:
            messages.append("email must not be blank!")
        if len(str(email)) < 2:
            messages.append("email must be at least 2 characters long!")
        if len(str(password)) < 1:
            messages.append("password must not be blank")
        if len(str(password)) < 8:
            messages.append("password must be at least 8 characters long!")
        if User.objects.filter(email=email):
            # encode the password to a specific format since the above email is registered
            login_pw = password.encode()
            # encode the registered user's password from database to a specific format
            db_pw = User.objects.get(email=email).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(login_pw, db_pw):
                messages.append("Password is Incorrect!")
        else:
            messages.append("Email has already been registered!")
        return messages

    def register(self, postData):
        print "register process"
        messages = []
        name = postData['name']
        if len(str(name)) < 1:
            messages.append("Error! Name must not be blank!")
        if len(str(name)) < 2:
            messages.append("Error! Name must be at least 2 characters long!")

        # last_name = postData['last_name']
        # if len(str(last_name)) < 1:
        #     messages.append("Error! Last name must not be blank!")
        # if len(str(last_name)) < 2:
        #     messages.append("Error! Last name must be at least 2 characters long!")

        alias = postData['alias']
        if len(str(alias)) < 1:
            messages.append("Error! Alias must not be blank!")
        if len(str(alias)) < 2:
            messages.append("Error! Alias must be at least 2 characters long!")

        email = postData['email']
        if len(str(email)) < 1:
            messages.append("Error! Email must not be blank!")
        if len(str(email)) < 2:
            messages.append("Error! Email must be at least 2 characters long!")
        if not EMAIL_REGEX.match(email):
            messages.append("Error! Email must be in a valid format!")

        password = postData['password']
        if len(str(password)) < 1:
            messages.append("Error! Password must not be blank!")
        if len(str(password)) < 8:
            messages.append("Error! Password must be at least 8 characters long!")

        pw_confirm = postData['pw_confirm']
        if pw_confirm != password:
            messages.append("Error! Passwords must match!")

        user_list = User.objects.filter(name=name)
        for user in user_list:
            print user.name
        if user_list:
            messages.append("Error! Username is already in the system!")
        if not messages:
            print "No messages"
            password = password.encode()
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password, salt)
            # password = password
            print "Create User"
            print hashed_pw
            User.objects.create(name=name, email=email, password=hashed_pw, birthday=postData['birthday'])
            print hashed_pw
            print User.objects.all()
            return None
        return messages

class QuoteManager(models.Manager):
    def validate(self, postData, user):
        errors = []
        quote = postData['quote']
        if len(str(quote)) < 10:
            return (False, "Quote must not be blank")
        quoteby = postData['quoteby']
        if len(str(quoteby)) < 3:
            return (False, "Quoted By must not be blank!")
        else:
            Quote.objects.create(quote=quote, quoteby=quoteby, creator=User.objects.get(id=user))
            return (True, "Quote Added to Database")
        return (True, "Your quote is valid!")

    def favorite(self, userid, quoteid):
        if len(Quote.objects.filter(id=quoteid, favorited__id=userid)) > 0:
            return(False, "Error! You favorited this item!")
        else:
            this_quote = Quote.objects.get(id=quoteid)
            this_user = User.objects.get(id=userid)
            this_quote.favorited.add(this_user)
        return (True, "You successfully added this to your favorites list!")

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pw_confirm = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Name: " + str(self.name) + ", Email: " + str(self.email) + ", Birthday: " + str(self.birthday)

class Quote(models.Model):
    quote = models.CharField(max_length=200)
    creator = models.ForeignKey(User)
    quoteby = models.CharField(max_length=200)
    favorited = models.ManyToManyField(User, related_name="user_favorite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Quote: " + str(self.quote) + ", Creator: " + str(self.creator) + ", Quote By: " + str(self.quoteby) + ", Favorited: " + str(self.favorited)
