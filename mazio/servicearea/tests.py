from decimal import Decimal

from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from servicearea.models import ServiceArea


class ServiceAreaResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['test_providers.json', 'test_service_areas.json']

    def setUp(self):
        super().setUp()
        self.base_url = '/api/v1/service_areas/'
        resp = self.api_client.get(self.base_url, format='json')
        self.service_area1 = ServiceArea.objects.get(
            pk=self.deserialize(resp)['objects'][0]['id']
        )
        self.service_area2 = ServiceArea.objects.get(
            pk=self.deserialize(resp)['objects'][1]['id']
        )
        self.detail_url1 = self.base_url + '{0}/'.format(self.service_area1.pk)
        self.detail_url2 = self.base_url + '{0}/'.format(self.service_area2.pk)

        self.post_data = {
            "name": "newrasdfasdoute",
            "polys": {
                "coordinates": [[[[1, 1], [1, 2], [2, 2], [1, 1]]]],
                "type": "MultiPolygon"
            },
            "price": "22.40",
            "provider": "/api/v1/providers/1/"
        }

    def test_GET_list_of_service_areas_json(self):
        resp = self.api_client.get(self.base_url, format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(self.deserialize(resp)['objects']), 2)
        self.assertKeys(
            self.deserialize(resp)['objects'][0],
            ('name', 'price', 'provider', 'polys', 'id', 'resource_uri'),
        )
        self.assertKeys(
            self.deserialize(resp)['objects'][1],
            ('name', 'price', 'provider', 'polys', 'id', 'resource_uri'),
        )
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': self.service_area1.pk,
            'name': self.service_area1.name,
            'provider': '/api/v1/providers/1/',
            'price': self.service_area1.price.to_eng_string(),
            'resource_uri': self.base_url+'{0}/'.format(self.service_area1.pk),
            'polys': {'coordinates': [[[[10.0, 10.0],
                        [10.0, 20.0],
                        [20.0, 20.0],
                        [20.0, 15.0],
                        [10.0, 10.0]]]],
                      'type': 'MultiPolygon'},
        })
        self.assertEqual(self.deserialize(resp)['objects'][1], {
            'id': self.service_area2.pk,
            'name': self.service_area2.name,
            'provider': '/api/v1/providers/1/',
            'price': self.service_area2.price.to_eng_string(),
            'resource_uri': self.base_url+'{0}/'.format(self.service_area2.pk),
            'polys': {'coordinates': [[[[1.0, 1.0], [1.0, 2.0],
                                        [2.0, 2.0], [1.0, 1.0]]]],
                      'type': 'MultiPolygon'}
        })

    def test_GET_service_area_details_json(self):
        resp = self.api_client.get(self.detail_url1, format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(
            self.deserialize(resp),
            ('name', 'price', 'provider', 'polys', 'id', 'resource_uri'),
        )
        self.assertEqual(self.deserialize(resp)['name'], self.service_area1.name)

        resp = self.api_client.get(self.detail_url2, format='json')
        self.assertValidJSONResponse(resp)
        self.assertKeys(
            self.deserialize(resp),
            ('name', 'price', 'provider', 'polys', 'id', 'resource_uri'),
        )
        self.assertEqual(self.deserialize(resp)['name'], self.service_area2.name)

    def test_POST_service_area(self):
        # Check how many are there first.
        self.assertEqual(ServiceArea.objects.count(), 2)
        self.assertHttpCreated(
            self.api_client.post(self.base_url, format='json',
                                 data=self.post_data)
        )
        # Verify a new one has been added.
        self.assertEqual(ServiceArea.objects.count(), 3)

    def test_PUT_service_area_detail(self):
        # Grab the current data & modify it slightly.
        original_data = self.deserialize(
            self.api_client.get(self.base_url+'1/', format='json'))
        new_data = original_data.copy()
        new_data['name'] = 'newName'
        new_data['price'] = 23.30

        self.assertEqual(ServiceArea.objects.count(), 2)
        self.assertHttpAccepted(
            self.api_client.put(self.base_url+'1/', format='json',
                                data=new_data))
        # Make sure the count hasn't changed & we did an update.
        self.assertEqual(ServiceArea.objects.count(), 2)
        # Check for updated data.
        self.assertEqual(ServiceArea.objects.get(pk=1).name, 'newName')
        self.assertAlmostEqual(ServiceArea.objects.get(pk=1).price, Decimal(23.3))

    def test_DELETE_detail(self):
        self.assertEqual(ServiceArea.objects.count(), 2)
        self.assertHttpAccepted(
            self.api_client.delete(self.base_url+'1/', format='json'))
        self.assertEqual(ServiceArea.objects.count(), 1)