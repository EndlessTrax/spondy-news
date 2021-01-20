from django.urls import reverse
from django.utils import timezone

import pytest
from pytest_django.asserts import assertTemplateUsed

from .models import Entry


@pytest.fixture
def test_entry(db):
    """Test article fixture"""
    entry = Entry.objects.create(
        title="Awesome Article Title",
        description="A great article about all the things.",
        pub_date=timezone.now(),
        link="http://myawesomeblog.com",
        category="ARTICLE",
    )
    return entry


def test_class_str_repr(test_entry):
    """Tests the models __str__ function"""
    assert str(test_entry) == "Awesome Article Title"


def test_entry_content(test_entry):
    """Tests the model saves content correctly"""
    assert test_entry.link == "http://myawesomeblog.com"
    assert test_entry.category == "ARTICLE"


@pytest.mark.django_db
def test_homepage_status_code(client):
    """Checks the response code of the homepage"""
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_homepage_uses_correct_template(client):
    """Check the correct template is used for the homepage"""
    response = client.get(reverse("homepage"))
    assertTemplateUsed(response, "homepage.html")
