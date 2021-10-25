from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Beverage)
admin.site.register(Bruger)
admin.site.register(Order)