from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_admin_action_publish_selected(client, example_entry):
    """Checks the that the custom admin function changes an entrys published status"""
    change_url = reverse("admin:aggregator_entry_change", args=(example_entry.id,))
    data = {"action": "publish_selected", "_selected_action": [example_entry.id]}
    response = client.post(change_url, data, follow=True)
    assert response.status_code == 200


def test_sitemap_status_code(client):
    """Checks the response code of sitemap.xml """
    response = client.get("/sitemap.xml")
    assert response.status_code == 200


def test_robots_txt_status_code(client):
    """Checks the response code of sitemap.xml """
    response = client.get("/robots.txt")
    assert response.status_code == 200


@pytest.mark.django_db
def test_rss_feed_latest_status_code(client):
    """Checks the response code of the RSS feed for latest entries"""
    response = client.get("/feeds/latest/rss.xml")
    assert response.status_code == 200