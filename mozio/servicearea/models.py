from django.contrib.gis.db import models as gis_models
from django.db import models

from provider.models import Provider


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, related_name='service_areas')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    polys = gis_models.MultiPolygonField(null=True, blank=True)
