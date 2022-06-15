from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models import F, Count


class Employee(models.Model):

    username = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    Department = models.CharField(max_length=20)
    Designation = models.CharField(max_length=20)
    line_manager = models.CharField(max_length=20)
    doj = models.DateField()
    address = models.CharField(max_length=500)
    pincode = models.IntegerField()

    def __str__(self):
        return f'{self.username}  || {self.mobile}|| {self.Department} || {self.Designation} || {self.line_manager} || {self.doj} || {self.address} || {self.pincode}'


class Supplier(models.Model):

    sid = models.IntegerField(primary_key=True)
    mobile = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    product_type = models.CharField(max_length=20)
    GST = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    pincode = models.IntegerField()

    def __str__(self):
        return f'{self.sid}  ||{self.name}  ||{self.email}  || {self.mobile}|| {self.product_type} || {self.GST} || {self.address} || {self.pincode}'


class Stock(models.Model):

    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_type = models.CharField(max_length=20)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dop = models.DateField()
    temp = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id} || {self.product_name} || {self.product_price} || {self.product_type} || {self.supplier} || {self.dop} || {self.temp}'

class Asset(models.Model):
    aid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100)
    depreciation = models.FloatField()
    warranty_date = models.DateField()
    status = models.IntegerField()
    age = models.IntegerField()
    depActive = models.IntegerField()

    def __str__(self):
        return f'{self.aid} || {self.serial_number} ||{self.depreciation} || {self.warranty_date} ||{self.status} || {self.age} ||{self.depActive}'

class Consumables(models.Model):
    cid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    old_quantity = models.IntegerField()
    old_expiry = models.DateField()
    new_quantity = models.IntegerField()
    new_expiry = models.DateField()
    min_count = models.IntegerField()

    def __str__(self):
        return f'{self.cid} || {self.old_quantity} ||{self.old_expiry} || {self.new_expiry} ||{self.new_quantity} || {self.min_count} '

class Scrap (models.Model):
    aid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    disposed_date = models.DateField()

    def __str__(self):
        return f'{self.aid} || {self.reason} ||{self.disposed_date}'

class Warranty(models.Model):
    aid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    price = models.FloatField()
    extension_date = models.DateField()

    def __str__(self):
        return f'{self.aid} || {self.price} ||{self.extension_date} '

class Service(models.Model):
    aid = models.ForeignKey(Stock,on_delete=models.CASCADE)
    price = models.FloatField()
    sent_date = models.DateField()
    received_date = models.DateField()

    def __str__(self):
        return f'{self.aid} || {self.price} ||{self.sent_date} || {self.received_date} '

class Allocation(models.Model):
    aid = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    allocated_date = models.DateField()
    return_date = models.DateField()
    returned = models.IntegerField()

    def __str__(self):
        return f'{self.aid} || {self.stock} ||{self.allocated_date} || {self.return_date} || {self.returned}'

class Allocation_approval(models.Model):
    all_req = models.IntegerField(primary_key=True)
    aid = models.ForeignKey(User,on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    request_date = models.DateField()
    reason = models.IntegerField()


    def __str__(self):
        return  f'{self.all_req} ||{self.aid} || {self.stock} ||{self.request_date} || {self.reason}'

class  Cash(models.Model):
    sid = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField()
    type = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.sid} || {self.price} ||{self.date} || {self.type}'


class Request(models.Model):
    id = models.IntegerField(primary_key=True)
    aid = models.ForeignKey(User,on_delete=models.CASCADE)
    request = models.CharField(max_length=500)
    validation = models.IntegerField()
    date = models.DateField()
    remark = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.id} ||{self.aid} || {self.request} ||{self.validation} || {self.date} || {self.remark}'











