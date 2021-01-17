from django.views.generic import ListView

from .models import Entry


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["articles"] = Entry.objects.filter(
            is_published=True, category="ARTICLE"
        ).order_by("-pub_date")[:25]

        context["researches"] = Entry.objects.filter(
            is_published=True, category="RESEARCH"
        ).order_by("-pub_date")[:25]
        
        context["events"] = Entry.objects.filter(
            is_published=True, category="EVENT"
        ).order_by("-pub_date")
        
        return context
