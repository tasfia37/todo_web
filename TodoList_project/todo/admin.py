from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields=('dateCreated',)    #this field can't be edited readonly

admin.site.register(Todo,TodoAdmin)

# Register your models here.
