from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed

from aggregator.management.commands.startjobs import delete_rejected_entries
from aggregator.models import Entry

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


@pytest.mark.django_db
def test_delete_rejected_entries_job(example_entry, example_old_entry):
    """Tests that the delete_rejected_entries function only deletes entries
    that have is_published=False and a pub_date older than 14 days."""
    assert Entry.objects.filter(title=example_entry.title).exists()
    assert Entry.objects.filter(title=example_old_entry.title).exists()
    
    # Delete only unpublished entries over 14 days old. 
    delete_rejected_entries()

    assert Entry.objects.filter(title=example_entry.title).exists()
    assert not Entry.objects.filter(title=example_old_entry.title).exists()





