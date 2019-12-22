from django.db import models
import datetime

# Create your models here.
class RateList(models.Model):
    usd = models.FloatField()

    class Meta:
        ordering = ('id', )


class Budget(models.Model):
    dollar_count = models.FloatField(default=11000000.)
    tenge = models.FloatField(default=0.)
    created_at = models.DateField()

class AgentsLog(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    prediction = models.FloatField()
    current = models.FloatField()
    real_price = models.FloatField()
    day = models.IntegerField()
    test_case = models.IntegerField()
    from_government = models.BooleanField(default=True)
    seller = models.CharField(max_length=50, null=True)
    buyer = models.CharField(max_length=50, null=True)
    quantity = models.FloatField()

    tenge = models.FloatField()
    dollar = models.FloatField()

    class Meta:
        ordering = ['-day']

class AgentsState(models.Model):
    name = models.CharField(max_length=50)
    day = models.IntegerField()
    test_case = models.IntegerField()
    is_seller = models.BooleanField(default=False)
    quantity = models.FloatField(default=0.)
    cost = models.FloatField()