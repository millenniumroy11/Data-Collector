from django.contrib import admin
from .models import DetailsForm

# Register your models here.
@admin.register(DetailsForm)
class DetailsAdmin(admin.ModelAdmin):
    list_display = ('fullname',  'email', 'address')  # Fields to display