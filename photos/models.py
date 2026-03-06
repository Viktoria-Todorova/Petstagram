from django.core.validators import MinLengthValidator
from django.db import models

from photos.validators import FileSizeValidator


# Create your models here.
class Photo(models.Model):
    photo =models.ImageField(
        upload_to="media",
        validators=[FileSizeValidator(5)]
    )
    description = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(10)],
        blank=True,
        null=True
    )

    location = models.CharField(max_length=30)
    tagged_pets =models.ManyToManyField(to= "pets.Pet")

    date_of_publication = models.DateField(auto_now=True)
