from django.db import models

class URLModel(models.Model):
    url = models.URLField(max_length=500)
