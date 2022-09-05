from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Package)
admin.site.register(Place)
admin.site.register(Tag)
admin.site.register(Day)
admin.site.register(Month)
admin.site.register(Wallet)
admin.site.register(Bookedtrip)
admin.site.register(Prevtrip)
admin.site.register(Transaction)