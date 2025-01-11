from django.contrib import admin
from userauths.models import User, ContectUs

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email', 'bio']

class ContactusAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'subject']
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ContectUs, ContactusAdmin)

