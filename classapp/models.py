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

    facebook_url = models.TextField(null=True)
    additional_email_1 = models.TextField(null=True)
    additional_email_2 = models.TextField(null=True)

    #user_picture goes here later

    USERNAME_FIELD = 'netid'
    objects = UVMUserManager()

class Course(models.Model):
    term = models.CharField(max_length=40)
    subject = models.CharField(max_length=10)
    number = models.IntegerField()
    crn = models.IntegerField()
    section = models.CharField(max_length=2)
    instructor = models.TextField()

    users = models.ManyToManyField("UVMUser")

class Post(models.Model):
    user = models.ForeignKey("UVMUser")
    course = models.ForeignKey("Course")
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey("UVMUser")
    post = models.ForeignKey("Post")
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
