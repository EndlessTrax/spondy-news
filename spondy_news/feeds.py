from django.contrib.syndication.views import Feed
from aggregator.models import Entry

import uuid


class LatestEntriesFeed(Feed):
    title = "Spondy News Feed"
    link = "https://spondy.news"
    description = "Published entries on Spondy News"

    def items(self):
        return Entry.objects.filter(is_published=True).order_by("-pub_date")[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_guid(self, obj):
        return str(uuid.uuid4())