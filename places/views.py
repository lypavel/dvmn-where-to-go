from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from places.models import Place


def index(request):
    places = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.lng, place.lat]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.id,
                    'detailsUrl': reverse(
                        'places',
                        kwargs={'place_id': place.id}
                    )
                }
            } for place in Place.objects.all().iterator()
        ]
    }

    return render(request, 'index.html', context={'places': places})


def place_page(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        pk=place_id
    )
    image_urls = [image.image.url for image in place.images.all()]

    return JsonResponse(
        {
            'title': place.title,
            'imgs': image_urls,
            'description_short': place.short_description,
            'description_long': place.long_description,
            'coordinates': {
                'lng': place.lng,
                'lat': place.lat
            }
        },
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 2
        }
    )
