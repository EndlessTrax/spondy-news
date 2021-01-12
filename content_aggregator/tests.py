import pytest

from django.utils import timezone

from .models import Entry


@pytest.fixture
def test_entry(db):
    entry = Entry.objects.create(
        title = "Awesome Article Title",
        description = "A great article about all the things.",
        pub_date = timezone.now(),
        link = "http://myawesomeblog.com",
        category = "ARTICLE"
    )
    return entry

def test_class_str_repr(test_entry):
    assert str(test_entry) == "Awesome Article Title"
