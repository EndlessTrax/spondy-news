from django.contrib.syndication.views import Feed
from aggregator.models import Entry


class LatestEntriesFeed(Feed):
    title = "Spondy News Feed"
    link = "https://spondy.news"
    description = "Published entries on Spondy News"

    def items(self):
        return Entry.objects.filter(is_published=True).order_by("-pub_date")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.link

    def item_categories(self, item):
        return [item.category]