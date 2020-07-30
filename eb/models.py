from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    Email = models.CharField(max_length=200, null=True)
    Society = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="no.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    Email = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    village = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    salary = models.CharField(max_length=100, null=True)
    skills = models.ManyToManyField(Skill)
    profile_pic = models.ImageField(default="no.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    worker = models.ForeignKey(Worker, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.worker.name


class Order(models.Model):
    Period = (
        ('1 month', ' 1 month'),
        ('6 month', '6 month'),
        ('1 year', '1 year'),
        ('15 days', '15 days'),
        ('1 day trial', '1 day trial'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    worker = models.ForeignKey(Worker, null=True, on_delete=models.SET_NULL)
    period_work = models.CharField(max_length=200, null=True, choices=Period)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.worker.name

