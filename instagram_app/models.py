from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Image(models.Model):
    User = models.TextField(null=True)
    image_url = models.TextField(null=True)
    image_link = models.TextField(null=True)
    image_datatype = models.TextField(null=True)
    post_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.User