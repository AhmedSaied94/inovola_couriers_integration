from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class UserManager(BaseUserManager):
    """
    class manager for providing a User(AbstractBaseUser) full control
    on this objects to create all types of User and this roles.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        pass data  to '_create_user' for creating normal_user .
        """
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        pass data to '_create_user' for creating super_user .
        """
        if email is None:
            raise TypeError("Users must have an email address.")
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_("Username"), max_length=255, unique=True)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    full_name = models.CharField(_("Full name"), max_length=255)
    activation_code = models.CharField(_("activation code"), max_length=50, null=True, blank=True, unique=True)

    is_active = models.BooleanField(_("Is active"), default=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)

    REQUIRED_FIELDS = ['email', 'full_name']
    USERNAME_FIELD = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
