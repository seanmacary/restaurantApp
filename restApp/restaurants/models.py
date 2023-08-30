from django.db import models


# Users Table
class Users(models.Model):
    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)  # Consider using Django's built-in User model for better security
    Email = models.EmailField()
    Created_at = models.DateTimeField(auto_now_add=True)
    LastLogin = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Users"


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
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    ReviewText = models.TextField()
    ReviewDate = models.DateTimeField(auto_now_add=True)
    Rating = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Reviews"


# UserPreferences Table
class UserPreferences(models.Model):
    PreferenceID = models.AutoField(primary_key=True)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    CuisinePreference = models.TextField()

    class Meta:
        verbose_name_plural = "UserPreferences"


# UserActions Table
class UserActions(models.Model):
    ActionID = models.AutoField(primary_key=True)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    Restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    ActionType = models.CharField(max_length=255)
    ActionDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "UserActions"
