from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    swift_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class LC(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    swift_code = models.CharField(max_length=50)
    global_limit = models.DecimalField(max_digits=20, decimal_places=2)
    lc_no = models.CharField(max_length=50)
    opening_date = models.DateField()
    lc_amount = models.DecimalField(max_digits=20, decimal_places=2)
    maturity_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='lc_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lc_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank.name} - {self.lc_no}"
