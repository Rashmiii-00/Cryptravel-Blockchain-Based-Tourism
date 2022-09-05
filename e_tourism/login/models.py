
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Details(models.Model):
    private_key = models.CharField(max_length=500, default=0)
    public_key = models.CharField(max_length=500, default=0)
    address = models.CharField(max_length=500, default=0)
    live_bitcoin_price = models.CharField(max_length=500,default=0)

class Tag(models.Model):
    name = models.CharField(max_length=200, null=False)
    tag_pic = models.ImageField(default="grouptour.jpg", blank="True")
    def __str__(self):
        return self.name

class Month(models.Model):
    name = models.CharField(max_length=20,null=False)
    def __str__(self):
        return self.name

class Package(models.Model):
    CATEGORY = (
        ('International', 'International'),
        ('Domestic', 'Domestic'),
    )
    package_pic = models.ImageField(default="andaman.jpg", null=True, blank="True")
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    nights = models.IntegerField(null=False,default=0)
    days = models.IntegerField(null=False,default=0)
    price = models.IntegerField(null=False,default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag,related_name='tags')
    months = models.ManyToManyField(Month,related_name='availmonths')

    def __str__(self):
        return self.name

class Place(models.Model):
    package = models.ForeignKey(to=Package,null=True, on_delete= models.SET_NULL)
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=500, null=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Day(models.Model):
    package = models.ForeignKey(to=Package, null=True, on_delete=models.SET_NULL)
    desc = models.TextField()
    day_pic = models.ImageField(default="andaman.jpg", blank="True")
    dayno = models.IntegerField()

class Wallet(models.Model):
    name = models.CharField(max_length=200, null=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Bookedtrip(models.Model):
    name = models.CharField(max_length=200, null=False)
    pname = models.CharField(max_length=200, null=False)
    month = models.CharField(max_length=200, null=False)
    price = models.IntegerField(null=False)
    pack_pic = models.ImageField(default="andaman.jpg", blank="True")

    def __str__(self):
        return self.pname

class Prevtrip(models.Model):
    name = models.CharField(max_length=200, null=False)
    pname = models.CharField(max_length=200, null=False)
    month = models.CharField(max_length=200, null=False)
    price = models.IntegerField(null=False)
    pack_pic = models.ImageField(default="andaman.jpg", blank="True")

    def __str__(self):
        return self.pname

class Transaction(models.Model):
    name = models.CharField(max_length=200, null=False)
    public_key = models.CharField(max_length=500, default=0, null=True)
    address = models.CharField(max_length=500, default=0)
    category = models.CharField(max_length=200, null=True)
    amount = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name+"-"+self.category





    


    
    