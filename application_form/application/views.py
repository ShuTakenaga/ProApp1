from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import context, loader
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Account
from .forms import AccountForm

from django.contrib.auth.models import User

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    # model = FirstModel
    # template_name = 'home'
    # context_object_name = 'account'
    # return render(request, 'home.html')
    
    # template = loader.get_template('home.html')
    # accounts = Account.objects.all
    
    user = request.user
    
    
    
    params = {
        'user' : user
    }
    
    # accounts = Account()
    # accounts.user = user
    # accounts.save()
    
    # accounts = FirstModel.objects.get(id == 9)
    
    # context = {
    #     'accounts' : accounts,
    # }
    
    # return HttpResponse(template.render(context, request))
    # return render(request, 'home.html', {accounts : accounts})
    
    return render(request, 'home.html', params)
    
@login_required
def account_create(request):
    # account = {}
        
    # account['form'] = AccountForm()
    
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        
        user = request.user
        
        account = account_form.save(commit=False)
        account.user = user
        
        account = Account(**account_form.cleaned_data)
        
        user.account.save()
        
        account.save()
        
        return redirect(to = '/')
    
    else:
        form = AccountForm()
    
    params = {
        'form' : form
    }
    
    return render(request, 'accountcreate.html', params)

@login_required
def company(request):
    return render(request, 'company.html')