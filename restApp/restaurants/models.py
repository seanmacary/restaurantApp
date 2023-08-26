from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    objects = models.Manager()

    # class Meta:
    #     db_table = 'restaurants'
