from django.db import models
import hashlib

def HashPassword(passwd):
    passwd += '&^@#&(*~!+)^'
    return hashlib.sha256(passwd.encode()).hexdigest()

class User(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    passwd = models.CharField(max_length=256)
