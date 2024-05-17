from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
        unique=True,
        db_index=True
    )

    short_description = models.TextField(
        'Краткое описание',
        blank=True
    )
    long_description = HTMLField(
        'Полное описание',
        blank=True
    )

    lng = models.FloatField(
        'Долгота'
    )
    lat = models.FloatField(
        'Широта'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        unique_together = ('title', 'id')


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место',
    )
    image = models.ImageField('Изображение')
    position = models.PositiveIntegerField(
        'Положение',
        default=0
    )

    def __str__(self) -> str:
        return f'{self.id} - {self.place.title}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['position']
