import binascii
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    LastLogin = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'UserName'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = "CustomUsers"


# Restaurants Table
class Restaurants(models.Model):
    RestaurantID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    ShortDescription = models.TextField()
    Cuisinetype = models.TextField()
    Address = models.CharField(max_length=255)
    Rating = models.FloatField()
    Latitude = models.FloatField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    TotalReview = models.PositiveIntegerField(default=0)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Restaurants"


# RestaurantImages Table
class RestaurantImages(models.Model):
    ImageID = models.AutoField(primary_key=True)
    Restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    ImageURL = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "RestaurantImages"


# Reviews Table
class Reviews(models.Model):
    ReviewID = models.AutoField(primary_key=True)
    Restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ReviewText = models.TextField()
    ReviewDate = models.DateTimeField(auto_now_add=True)
    Rating = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Reviews"


# UserPreferences Table
class UserPreferences(models.Model):
    PreferenceID = models.AutoField(primary_key=True)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CuisinePreference = models.TextField()

    class Meta:
        verbose_name_plural = "UserPreferences"


# UserActions Table
class UserActions(models.Model):
    ActionID = models.AutoField(primary_key=True)
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    ActionType = models.CharField(max_length=255)
    ActionDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "UserActions"


class UserToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='user_auth_token',  # Change this line
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
