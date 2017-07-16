from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource

from provider.api.resources import ProviderResource
from servicearea.models import ServiceArea


class ServiceAreaResource(ModelResource):
    provider = fields.ForeignKey(ProviderResource, 'provider')

    class Meta:
        resource_name = 'service_areas'
        queryset = ServiceArea.objects.all()

        filtering = {
            'polys': 'ALL',
        }
