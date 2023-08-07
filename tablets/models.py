from django.db import models

# Create your models here.

class Tokens(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    expiration_date = models.DateTimeField()

class PublicacionData(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField(blank=True)
    condition = models.TextField(blank=True)
    price = models.IntegerField(blank=True)
    permalink = models.TextField(blank=True)
    thumbnail = models.TextField(blank=True)
    sold_quantity = models.IntegerField(blank=True)
    available_quantity = models.IntegerField(blank=True)
    seller_id = models.TextField(blank=True)
    seller_nickname = models.TextField(blank=True)
    brand = models.TextField(blank=True)
    line = models.TextField(blank=True)
    model = models.TextField(blank=True)
    shipping = models.BooleanField(blank=True)
    visits_last_month = models.IntegerField(blank=True)
    date_retrieved = models.DateTimeField()
    
class Notebooks(PublicacionData):
    pass  # No es necesario agregar campos adicionales para Notebooks

class Tablets(PublicacionData):
    pass  # No es necesario agregar campos adicionales para Tablets

class PCs(PublicacionData):
    pass  # No es necesario agregar campos adicionales para PCs

class Impresoras(PublicacionData):
    pass  # No es necesario agregar campos adicionales para Impresoras