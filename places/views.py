from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from places.models import Image, Place


def index(request):
    geo_json = {
        'type': 'FeatureCollection',
        'features': []
    }

    for place in Place.objects.all().iterator():
        geo_json['features'].append(
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.lng, place.lat]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.slug,
                    'detailsUrl': 'static/places/moscow_legends.json'
                }
            }
        )

    data = {'places': geo_json}
    return render(request, 'index.html', context=data)


def place_page(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    images = Image.objects.filter(place__id=place_id)
    image_urls = [image.image.url for image in images]

    return JsonResponse(
        {
            'title': place.title,
            'imgs': image_urls,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': {
                'lng': place.lng,
                'lat': place.lat
            }
        },
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        })
