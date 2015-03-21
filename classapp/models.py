from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

class UVMUserManager(BaseUserManager):
    def _create_user(self, netid, password, first_name=None, last_name=None, uvm_email=None, full_name=None, department=None):
        if not netid:
            raise ValueError("Netid must be set")

        user = self.model(netid=netid, first_name=first_name, last_name=last_name, full_name=full_name, department=department)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, netid, password=None, **extra_fields):
        return self._create_user(netid,password, **extra_fields)

    def create_superuser(self, netid, password=None, **extra_fields):
        return self._create_user(netid, password, **extra_fields)

class UVMUser(AbstractBaseUser):
    netid = models.CharField(max_length=8,unique=True)
    first_name = models.CharField(max_length=40,null=True)
    last_name = models.CharField(max_length=40,null=True)
    uvm_email = models.CharField(max_length=40,null=True)
    full_name = models.CharField(max_length=150,null=True)
    department = models.CharField(max_length=40,null=True)

    USERNAME_FIELD = 'netid'
    objects = UVMUserManager()

