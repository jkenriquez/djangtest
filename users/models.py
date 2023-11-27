from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
import random, os



def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    user_name = instance.first_name.title()+' '+instance.middle_name[0].upper()+' '+instance.last_name.title()
    _now = datetime.now()
    return 'users/{user_name}/profile_pict/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(user_name=user_name,imageid = instance, basename=basefilename, randomstring = randomstr,ext = file_extension,year=_now.strftime('%Y'),month=_now.strftime('%m'),day=_now.strftime('%d'))

class StaffManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=200,verbose_name='First Name')
    last_name = models.CharField(max_length=200,verbose_name='Last Name')
    middle_name = models.CharField(max_length=200,verbose_name='Middle Name')
    suffix_name = models.CharField(max_length=200,verbose_name='Suffix',default='',blank=True)
    image = models.ImageField(upload_to=image_path, default='profile_pict/image.jpg')
    is_active = models.BooleanField(default=True)
    is_provider = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    objects = StaffManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def get_all_permissions(self, obj=None):
        return set()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin