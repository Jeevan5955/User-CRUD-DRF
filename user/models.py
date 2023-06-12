from django.db import models

# Create your models here.



class User(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    mobileNumber = models.BigIntegerField()
    age = models.BigIntegerField()
    height = models.BigIntegerField()
    profilePicture =  models.URLField()


    class Meta:
        db_table = 'User'
        verbose_name = 'User Details'
