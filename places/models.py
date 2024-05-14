from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Уникальный id', unique=True)

    description_short = models.TextField(
        'Краткое описание',
        blank=True
    )
    description_long = models.TextField(
        'Полное описание',
        blank=True
    )

    lng = models.FloatField(
        'Долгота',
        blank=True
    )
    lat = models.FloatField(
        'Широта',
        blank=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['title']


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место',
    )
    image = models.ImageField('Изображение')

    def __str__(self) -> str:
        return f'{self.id} - {self.place.title}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['id']
