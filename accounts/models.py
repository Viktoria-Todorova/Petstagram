
from django.contrib.auth.base_user import AbstractBaseUser

from django.contrib.auth.models import PermissionsMixin
from django.db import models

from accounts.managers import AppUserManager


# Create your models here.

# create a custom user model inheriting from the AbstractBaseUser Django class. The model consists of the following fields:
#
# · email - email field, required and unique.
#
# · is_active - boolean field with default value True.
#
# · is_staff - boolean field with default value False.
#
# USERNAME_FIELD - specifies the field to be used as the unique identifier for authentication, which is email.
#
# REQUIRED_FIELDS - an empty list, implying that no additional fields are required when creating a user.
class AppUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD= 'email'
    email =models.EmailField(
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )
    object =AppUserManager()

    def __str__(self):
        return self.email


# Now we are going to link our AppUser with a custom Petstagram profile. Create a new model called Profile:
#
# · user - one-to-one field, primary key, with CASCADE delete option.
#
# · first_name - character field, with maximum of 30 characters, optional.
#
# · last_name - character field, with maximum of 30 characters, optional.
#
# · date_of_birth - date field, optional.
#
# · profile_picture - URL field, optional.

class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    profile_picture = models.URLField(
        null=True,
        blank=True,
    )
    @property
    def get_full_name(self)->str:

        return f'{self.first_name} {self.last_name}'
