from django.contrib import admin
from django.utils.html import format_html

from places.models import Place, Image


class PlaceImageInline(admin.TabularInline):
    model = Image
    extra = 1

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        max_height = 200
        return format_html(
            '<img src="{url}" width="{width}" height="{height}" />',
            url=obj.image.url,
            width=obj.image.width / (obj.image.height / max_height),
            height=max_height
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'lng', 'lat',)
    inlines = (PlaceImageInline,)
