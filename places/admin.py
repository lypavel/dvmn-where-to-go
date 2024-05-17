from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from places.models import Place, Image


class PlaceImageInline(SortableTabularInline):
    model = Image
    extra = 1

    readonly_fields = ('show_image_preview',)

    def show_image_preview(self, obj: Image):
        max_height = 200
        return format_html(
            '<img src="{url}" '
            'style="max-width:{width}px;max-height:{height}px" />',
            url=obj.image.url,
            width=obj.image.width / (obj.image.height / max_height),
            height=max_height
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'lng', 'lat',)
    inlines = (PlaceImageInline,)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ('place',)
