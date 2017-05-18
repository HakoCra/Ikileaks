from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class IkiliCommitterManager(BaseUserManager):

    def create_user(self, twitter_id, password=None, **extra_fields):
        if not twitter_id:
            raise ValueError('The Email must be set')
        user = self.model(twitter_id=twitter_id, **extra_fields)
        user.set_password(password or '')
        user.save()
        return user

    def create_superuser(self, twitter_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(twitter_id, password, **extra_fields)


class IkiliCommitter(AbstractBaseUser, PermissionsMixin):
    twitter_id = models.CharField(max_length=32, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'twitter_id'

    objects = IkiliCommitterManager()

    def get_full_name(self):
        return self.twitter_id

    def get_short_name(self):
        return self.twitter_id


class IkiliManager(models.Manager):

    def get_top_ikili_list(self):
        return self.order_by('-created_at')[:5]


class Ikili(models.Model):
    tweet_id = models.CharField(max_length=64, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = IkiliManager()


class Ikitterune(models.Model):
    ikili = models.ForeignKey(Ikili, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
