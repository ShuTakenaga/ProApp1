from django.contrib import admin
from .models import Account, Company, Application

# Register your models here.

admin.site.register(Account)
admin.site.register(Company)
admin.site.register(Application)
