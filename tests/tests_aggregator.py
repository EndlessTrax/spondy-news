from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed


def test_class_str_repr(example_entry):
    """Tests the models __str__ function"""
    assert str(example_entry) == "Awesome Article Title"


def test_entry_content(example_entry):
    """Tests the model saves content correctly"""
    assert example_entry.link == "http://myawesomeblog.com"
    assert example_entry.category == "ARTICLE"


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







