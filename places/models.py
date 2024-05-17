from django.db import models
from pytils.translit import slugify
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        'Уникальный id',
        unique=True,
        blank=True,
        max_length=200
    )

    description_short = models.TextField(
        'Краткое описание',
        blank=True
    )
    description_long = HTMLField(
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        unique_together = ('title', 'slug')


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
