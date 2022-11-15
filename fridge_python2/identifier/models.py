from django.db import models

# Create your models here.
class api(models.Model):
    current_items = models.CharField(max_length=200)
    in_and_out = models.CharField(max_length=200) 
    exp = models.CharField(max_length=200)
    fifo = models.CharField(max_length=200)
