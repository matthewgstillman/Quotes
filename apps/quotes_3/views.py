from django.shortcuts import render, redirect

from .models import User, Quote
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'quotes_3/index.html')

def register(request):
    #print request.POST
    if request.method == 'POST':
        messages = User.objects.register(request.POST)
        #Above line might be postData
    if not messages:
        print "No messages! Success!"
        # fetch user id and name via email
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/quotes')
    else:
        request.session['messages'] = messages
        print messages
    return redirect('/')

def login(request):
    users = User.objects.all()
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password'],
    }
    if request.method == 'POST':
        messages = User.objects.login(request.POST)
    if not messages:
        print "No messages! Success!"
        user_list = User.objects.all().filter(email=request.POST['email'])
        request.session['id'] = user_list[0].id
        request.session['name'] = user_list[0].name
        return redirect('/quotes')
    else:
        request.session['messages'] = messages
        return redirect('/')

def add_quote(request):
    if request.method == 'POST':
        result = Quote.objects.validate(request.POST, request.session['id'])
        if result[0]:
            messages.info(request, result[1])
            return redirect('/quotes')
        messages.error(request, result[1])
        return redirect('/quotes')

def add_fave(request, quoteid):
    favoritelist = Quote.objects.favorite(request.session['id'], quoteid)
    return redirect('/quotes')

def delete_fave(request, quoteid):
    if request.method == 'POST':
        remove = User.objects.get(id=request.session['id'])
        this_quote = Quote.objects.get(quoteid=id)
        remove.user_favorite.remove(this_quote)
        return redirect('/quotes')


def quotes(request):
    quotes = Quote.objects.all().order_by('-id')[:5]
    allquotes = Quote.objects.all()
    context = {
        'quotes': quotes,
        'allquotes': allquotes,
        'favoritelist': Quote.objects.filter(favorited=User.objects.get(id=request.session['id']))
    }
    print allquotes
    return render(request, 'quotes_3/quotes.html', context)

def users(request, id):
    quote = Quote.objects.get(id=id).creator.id
    counts = len(Quote.objects.filter(creator__id=quote))
    allquotes = Quote.objects.filter(creator__id=quote).order_by('-created_at')
    context = {
        'loguser': User.objects.get(id=request.session['id']),
        'allquotes': allquotes,
        'quotecreator': quote,
        'creator': allquotes[0].creator.name,
        'counts': counts
    }
    return render(request, 'quotes_3/users.html', context)
