from django.shortcuts import render, redirect
from .models import *
from ..login_app.models import *
from django.contrib import messages

def index(req):
    if 'id' not in req.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=req.session['id'])
    }
    context['quotes'] = Quote.objects.exclude(favoritedby=context['user'])
    context['favorites'] = Quote.objects.filter(favoritedby=context['user'])
    return render(req, 'quotes/index.html', context)

def addquote(req):
    if 'id' not in req.session:
        return redirect('/')
    if req.method == "POST":
        d = req.POST
        errors = Quote.objects.validate_quote(d)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(req, error, extra_tags=tag)
        else:
            Quote.objects.create_quote(d, req.session['id'])
    return redirect('/quotes')

def favorite(req, quoteid):
    if 'id' not in req.session:
        return redirect('/')
    Quote.objects.add_favorite(quoteid, req.session['id'])
    return redirect('/quotes')

def unfavorite(req, quoteid):
    if 'id' not in req.session:
        return redirect('/')
    Quote.objects.remove_favorite(quoteid, req.session['id'])
    return redirect('/quotes')