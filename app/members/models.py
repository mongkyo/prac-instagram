from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    img_profile = models.ImageField(
        upload_to='user',
    )
    name = models.CharField(max_length=30)
    site = models.URLField(max_length=150)
    introduce = models.TextField(blank=True)

    def __str__(self):
        return self.name
