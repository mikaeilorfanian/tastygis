from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from provider.models import Provider


class ProviderResource(ModelResource):
    class Meta:
        queryset = Provider.objects.all()
        resource_name = 'provider'
        authorization = Authorization()
