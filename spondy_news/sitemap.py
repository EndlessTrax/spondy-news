from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["homepage"]

    def location(self, item):
        return reverse(item)
