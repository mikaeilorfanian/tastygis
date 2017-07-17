#### Intro
This project uses some great tools(Django, PostGIS, tastypie, swagger) to turn a hard problem into an easy one to solve.   
As you can see in the modules, I only had to write 15 lines of custom code to create an API that can handle:
* `PUT GET POST DELTE` operations for a `Provider` resource
* `PUT GET POST DELTE` operations for a `ServiceArea` resource
* Many standard spatial filters on the `ServiceArea` resource

#### Limitations
I deployed this solution to an Amazon EC2 instance. Security and speed of the server were not my focus.   
The speed of operations on the database, however, was my focus and I believe I've achieved this by simply using `PostgreSQL` + `PostGIS`.   
Please note that I've set `DEBUG` to `True` in Django settings and everything is being served by the built-in Django webserver.  
A more robust solution would call for tools like Gunicorn, nginx, and supervisor. Once again, I belive these to be out of the scope of this problem.  

#### How to Use the API  
I'm using Swagger to document *almost* all possible operations. Please visit [this url](http://52.14.61.103:8000/api/doc) to see the API documentation.   
Yet, some of the operations can be better visualized here due to limitations in `django-tastypie-swagger`.  
##### Changing the ServiceArea Resource  
The `polys` field of the `ServiceArea` resource takes a `MultiPolygon` geometry object which is tricky to build a JSON object for.  
Here's a sample payload for making a `POST` call that adds a service area resource:  
URL: [http://52.14.61.103:8000/api/v1/service_areas/](http://52.14.61.103:8000/api/v1/service_areas/)  
payload:  
```json
{
  "name": "newrasdfasdoute",
  "polys": {
    "coordinates": [
      [
        [
          [
            1,
            1
          ],
          [
            1,
            2
          ],
          [
            2,
            2
          ],
          [
            1,
            1
          ]
        ]
      ]
    ],
    "type": "MultiPolygon"
  },
  "price": "22.40",
  "provider": "/api/v1/providers/1/"
}
```  
Note that you need to have a `provider` with ID `1` before you can create the above service area resource.  

##### `contains` and Other GeoDjango Spatial Filters  
Not only you can do a `contains` query, other standard GeoDjango filters are also supported. All this is possible because `django-tastypie` has native support for `GeoDjango`.   
Here's a sample `GET` call for the `contains` filter:     
GET`http://52.14.61.103:8000/api/v1/service_areas/?polys__contains={"type": "Point", "coordinates": [-122.475233, 37.768617]}`   

This call returns polygons that contain the `point` given:  
```json
{
    "meta": {
        "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1},
    "objects": [
        {
            "name": "randomName",
            "id": "1",
            "polys": {
                "coordinates": [[[
                    [-122.511067, 37.771276], [-122.510037, 37.766390999999999],
                    [-122.510037, 37.763812999999999], [-122.456822, 37.765847999999998],
                    [-122.45296, 37.766458999999998], [-122.454848, 37.773989999999998],
                    [-122.475362, 37.773040000000002], [-122.511067, 37.771276]
                ]]],
                "type": "MultiPolygon"
            },
            "resource_uri": "/api/v1/service_areas/1/",
            "provider": 1
        }
    ]
}
```
