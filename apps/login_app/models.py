from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class MrManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['name']) < 2:
            errors['namelen'] = "Name must be at least two characters."
        if not data['name'].replace(' ','').replace('.', '').replace('-', '').isalpha():
            errors['namechars'] = "Names can only contain letters, spaces, periods, and dashes."
        if len(data['alias']) < 2:
            errors['aliaslen'] = "Alias must be at least two characters."
        if not data['alias'].isalnum():
            errors['aliaschars'] = "Alias may only contain letters and numbers."
        if not EMAIL_REGEX.match(data['email']) or len(data['email']) > 255:
            errors['email'] = "Not a valid email."
        if len(data['pword']) < 8:
            errors['pwlen'] = "Password must be at least 8 characters."
        if data['pword'] != data['conf']:
            errors['pwconf'] = "Password did not match confirmation."
        bday = datetime.datetime.strptime(data['bday'], '%Y-%m-%d')
        if not isinstance(bday, datetime.datetime):
            errors['bdaytype'] = "That is not a valid date."
        elapsed = datetime.datetime.now() - bday
        elapsed = divmod(elapsed.total_seconds(), 31536000)
        if elapsed[0] < 13:
            errors['bdaytime'] = "You must be at least 13 years old to use this website."
        return errors

    def create_user(self, data):
        bday = datetime.datetime.strptime(data['bday'], '%Y-%m-%d')
        user = self.create(name=data['name'], alias=data['alias'], email=data['email'], pword=bcrypt.hashpw(data['pword'].encode(), bcrypt.gensalt()), bday=bday)
        return user

    def login(self, data):
        if self.filter(email=data['email']).exists():
            user = self.get(email=data['email'])
            errors = {}
            if bcrypt.checkpw(data['pword'].encode(), user.pword.encode()):
                return {'status': True, 'user': user}
            else:
                errors['login'] = "Login information invalid."
        else:
            errors['login'] = "Login information invalid."
        return {'status': False, 'errors': errors}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255, unique=True)
    pword = models.CharField(max_length=255)
    bday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MrManager()