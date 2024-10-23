from django.db import models


# Create your models here.
class Client(models.Model):
    email = models.TextField(blank=False)
    password = models.TextField(blank=False)

    def __str__(self):
        return f'{self.email} - {self.password}'
