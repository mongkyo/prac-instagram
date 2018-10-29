from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='user',
        blank=True
    )
    site = models.URLField('사이트', max_length=150, blank=True)
    introduce = models.TextField('소개', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def img_profile_url(self):
        if self.img_profile:
            return self.img_profile.url
        return static('images/blank_user.png')

    def like_post_toggle(self, post):
        # if self.postlike_set.filter(post=post).exists():
        #     self.postlike_set.filter(post=post).delete()
        # else:
        #     self.postlike_set.create(post=post)

        postlike, postlike_created = self.postlike_set.get_or_create(post=post)
        if not postlike_created:
            postlike.delete()
