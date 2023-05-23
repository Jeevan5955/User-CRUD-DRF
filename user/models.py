from django.db import models

# Create your models here.



class User(models.Model):
    email = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    mobileNumber = models.BigIntegerField()
    age = models.BigIntegerField()
    height = models.BigIntegerField()


    class Meta:
        db_table = 'User'
        verbose_name = 'User Details'
