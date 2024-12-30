from django.db import models

# Create your models here.

class DetailsForm(models.Model):
    fullname=models.CharField(max_length=30)
    #mobile=models.CharField(max_length=15)
    email=models.EmailField(max_length=100)
    address=models.CharField(max_length=250)

    def __str__(self):
        return self.fullname