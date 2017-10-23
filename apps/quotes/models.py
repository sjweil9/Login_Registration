from __future__ import unicode_literals

from django.db import models
from ..login_app.models import *

class MrQuoteManager(models.Manager):
    def validate_quote(self, data):
        errors = {}
        if len(data['quoteby']) < 4:
            errors['quotebylen'] = "Quoted by field must be at least 4 characters."
        if not data['quoteby'].replace(' ', '').replace('.', '').replace('-', '').isalpha():
            errors['quotebychars'] = "Quoted by field may only contain letters, spaces, periods, and dashes."
        if len(data['quotetext']) < 11:
            errors['quotetextlen'] = "Quote message must be more than 10 characters."
        return errors

    def create_quote(self, data, userid):
        user = User.objects.get(id=userid)
        self.create(quoteby=data['quoteby'], quotetext=data['quotetext'], postedby=user)
        return True

    def add_favorite(self, quoteid, userid):
        if self.filter(id=quoteid).exists():
            quote = self.get(id=quoteid)
            user = User.objects.get(id=userid)
            quote.favoritedby.add(user)
            quote.save()
            return True
        else:
            return False
    
    def remove_favorite(self, quoteid, userid):
        if self.filter(id=quoteid).exists():
            quote = self.get(id=quoteid)
            user = User.objects.get(id=userid)
            quote.favoritedby.remove(user)
            quote.save()
            return True
        else:
            return False

class Quote(models.Model):
    quoteby = models.CharField(max_length=45)
    quotetext = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    postedby = models.ForeignKey(User, related_name="posted_quotes")
    favoritedby = models.ManyToManyField(User, related_name="favorites", default=None)
    objects = MrQuoteManager()