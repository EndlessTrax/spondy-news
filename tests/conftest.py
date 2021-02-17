import pytest
from django.utils import timezone

from aggregator.models import Entry


@pytest.fixture
def example_entry(db):
    """Test article fixture"""
    entry = Entry.objects.create(
        title="Awesome Article Title",
        description="A great article about all the things.",
        pub_date=timezone.now(),
        link="http://myawesomeblog.com",
        category="ARTICLE",
    )
    return entry
