import logging
import time
from urllib.parse import urljoin, urlsplit, unquote

from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
import requests as rq

from places.models import Place, Image

logging.basicConfig(
    filename='load_places.log',
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s %(filename)s  %(funcName)s]: '
           '%(message)s ',
    filemode='w',
    datefmt='%m/%d/%Y %H:%M:%S',
    encoding='utf-8'
)

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    help = 'Downloads json files and adds data to database.'

    def add_arguments(self, parser) -> None:
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--json_url',
            type=str,
            help='Json file url'
        )

        group.add_argument(
            '--json_github_urls',
            type=str,
            help='Url of GitHub directory containing json-files'
        )

    def parse_github_dir(self, html: str) -> set[str]:
        soup = BeautifulSoup(html, 'lxml')

        json_links = soup.select('.react-directory-truncate a')

        return {url['href'] for url in json_links}

    def save_place_in_db(self, place: dict) -> None:
        db_place, is_created = Place.objects.get_or_create(
            title=place['title'],
            defaults={
                'short_description': place['description_short'],
                'long_description': place['description_long'],
                'lng': place['coordinates']['lng'],
                'lat': place['coordinates']['lat']
            }
        )

        if not is_created:
            logger.info(
                f'Object \"{place["title"]}\" already exists in database.'
            )
            return

        logger.info(f'Object \"{place["title"]}\" successfully created.')

        for image_url in place['imgs']:
            img_name = urlsplit(unquote(image_url)).path.split('/')[-1]

            response = rq.get(image_url)
            response.raise_for_status()

            Image.objects.get_or_create(
                place=db_place,
                image=ContentFile(response.content, img_name),
            )
        logger.info(
            f'Images for object \"{place["title"]}\" successfully created.'
        )

    def handle(self, *args, **options) -> None:
        json_github_dir = options.get('json_github_urls')
        json_url = options.get('json_url')

        if json_github_dir:
            while True:
                response = rq.get(json_github_dir)
                response.raise_for_status()

                json_urls = self.parse_github_dir(response.text)

                if not json_urls:
                    logger.error(f'Can\'t get data from {json_github_dir}.')
                    logger.info('Trying to reconnect...')
                    time.sleep(10)
                    continue
                break

            places = []
            github_raw_url = 'https://raw.githubusercontent.com/'
            for json_url in json_urls:
                url = urljoin(github_raw_url, json_url).replace('/blob/', '/')
                response = rq.get(url)
                response.raise_for_status()

                places.append(response.json())

            for place in places:
                self.save_place_in_db(place)

        elif json_url:
            response = rq.get(json_url)
            response.raise_for_status()

            self.save_place_in_db(response.json())
