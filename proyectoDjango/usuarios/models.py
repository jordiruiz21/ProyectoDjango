from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el correo electrónico proporcionado."""
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    birthdate = models.DateField(blank=True, null=True)


    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email