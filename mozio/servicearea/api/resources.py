from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from provider.api.resources import ProviderResource
from servicearea.models import ServiceArea


class ServiceAreaResource(ModelResource):
    provider = fields.ForeignKey(ProviderResource, 'provider')

    class Meta:
        resource_name = 'service_areas'
        queryset = ServiceArea.objects.all()
        authorization = Authorization()

        filtering = {
            'polys': ALL,
        }
