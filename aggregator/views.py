from django.views.generic import ListView

from .models import Entry


class HomePageView(ListView):
    """Main homepage view"""

    template_name = "homepage.html"
    model = Entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filters the newest 25 articles to be displayed on homepage
        context["articles"] = Entry.objects.filter(
            is_published=True, category="ARTICLE"
        ).order_by("-pub_date")[:25]

        # Filters the newest 25 research article to be displayed on homepage
        context["researches"] = Entry.objects.filter(
            is_published=True, category="RESEARCH"
        ).order_by("-pub_date")[:25]

        # Filters all events to be displayed on homepage
        context["events"] = Entry.objects.filter(
            is_published=True, category="EVENT"
        ).order_by("-pub_date")

        return context
