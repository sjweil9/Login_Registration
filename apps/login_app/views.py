from django.shortcuts import render, redirect
from .models import *
from ..quotes.models import *
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(req):
    return render(req, 'login_app/index.html')

def register(req):
    if req.method == "POST":
        d = req.POST
        errors = User.objects.validator(d)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(req, error, extra_tags=tag)
        else:
            user = User.objects.create_user(d)
            req.session['id'] = user.id
            req.session['status'] = 'register'
            return redirect('/quotes')
    return redirect('/')

def login(req):
    if req.method == "POST":
        d = req.POST
        if EMAIL_REGEX.match(d['email']):
            res = User.objects.login(d)
            if res['status']:
                req.session['id'] = res['user'].id
                req.session['status'] = 'login'
                return redirect('/quotes')
            else:
                for tag, error in res['errors'].iteritems():
                    messages.error(req, error, extra_tags=tag)
        else:
            messages.error(req, 'Login information invalid.', extra_tags="login")
    return redirect('/')

def showuser(req, userid):
    if not User.objects.filter(id=userid).exists():
        return redirect('/quotes')
    context = {
        'user': User.objects.get(id=userid)
    }
    context['quotes'] = Quote.objects.filter(postedby=context['user'])
    return render(req, 'login_app/user.html', context)

def logout(req):
    req.session.clear()
    return redirect('/')