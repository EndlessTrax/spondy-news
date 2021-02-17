from django.contrib import admin

from .models import Entry


def publish_selected(modeladmin, request, queryset):
    queryset.update(is_published=True)


publish_selected.short_description = "Publish the selected posts"


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("pub_date", "title", "category", "is_featured", "is_published")
    actions = [publish_selected]
    ordering = ("-pub_date",)
