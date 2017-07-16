from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from provider.models import Provider


class ProviderResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['test_providers.json']

    def setUp(self):
        super().setUp()
        self.base_url = '/api/v1/providers/'
        resp = self.api_client.get(self.base_url, format='json')
        self.provider1 = Provider.objects.get(
            pk=self.deserialize(resp)['objects'][0]['id']
        )
        self.provider2 = Provider.objects.get(
            pk=self.deserialize(resp)['objects'][1]['id']
        )
        self.detail_url1 = self.base_url + '{0}/'.format(self.provider1.pk)
        self.detail_url2 = self.base_url + '{0}/'.format(self.provider2.pk)

        self.post_data = {
            'name': 'John',
            'email': 'johndoe@gmail.com',
            'phone': 1234567,
            'language': 'pl',
            'currency': 'pln',
        }

    def test_GET_list_of_providers_json(self):
        resp = self.api_client.get(self.base_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 2)
        self.assertKeys(
            self.deserialize(resp)['objects'][0],
            ('name', 'email', 'phone', 'language',
             'currency', 'resource_uri', 'id'),
        )
        self.assertKeys(
            self.deserialize(resp)['objects'][1],
            ('name', 'email', 'phone', 'language',
             'currency', 'resource_uri', 'id'),
        )
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': self.provider1.pk,
            'currency': self.provider1.currency,
            'name': self.provider1.name,
            'email': self.provider1.email,
            'language': self.provider1.language,
            'phone': self.provider1.phone,
            'resource_uri': self.base_url+'{0}/'.format(self.provider1.pk)
        })
        self.assertEqual(self.deserialize(resp)['objects'][1], {
            'id': self.provider2.pk,
            'currency': self.provider2.currency,
            'name': self.provider2.name,
            'email': self.provider2.email,
            'language': self.provider2.language,
            'phone': self.provider2.phone,
            'resource_uri': self.base_url+'{0}/'.format(self.provider2.pk)
        })

    def test_GET_provider_details_json(self):
        resp = self.api_client.get(self.detail_url1, format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(
            self.deserialize(resp),
            ('name', 'email', 'phone', 'language',
             'currency', 'resource_uri', 'id')
        )
        self.assertEqual(self.deserialize(resp)['name'], self.provider1.name)

        resp = self.api_client.get(self.detail_url2, format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(
            self.deserialize(resp),
            ('name', 'email', 'phone', 'language',
             'currency', 'resource_uri', 'id')
        )
        self.assertEqual(self.deserialize(resp)['name'], self.provider2.name)

    def test_POST_provider(self):
        # Check how many are there first.
        self.assertEqual(Provider.objects.count(), 2)
        self.assertHttpCreated(
            self.api_client.post(self.base_url, format='json',
                                 data=self.post_data)
        )
        # Verify a new one has been added.
        self.assertEqual(Provider.objects.count(), 3)

    def test_PUT_provider_detail(self):
        # Grab the current data & modify it slightly.
        original_data = self.deserialize(
            self.api_client.get(self.base_url+'1/', format='json'))
        new_data = original_data.copy()
        new_data['name'] = 'newName'
        new_data['email'] = 'newemail@go.com'

        self.assertEqual(Provider.objects.count(), 2)
        self.assertHttpAccepted(
            self.api_client.put(self.base_url+'1/', format='json',
                                data=new_data))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(Provider.objects.count(), 2)
        # Check for updated data.
        self.assertEqual(Provider.objects.get(pk=1).name, 'newName')
        self.assertEqual(Provider.objects.get(pk=1).email, 'newemail@go.com')

    def test_DELETE_detail(self):
        self.assertEqual(Provider.objects.count(), 2)
        self.assertHttpAccepted(
            self.api_client.delete(self.base_url+'1/', format='json'))
        self.assertEqual(Provider.objects.count(), 1)
