from django.db import models

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class NewUser(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()