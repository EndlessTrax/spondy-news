from django.views.generic import ListView

from .models import Entry


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = Entry.objects.filter().order_by("-pub_date")
        return context
