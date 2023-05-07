import os
import pytest
from django.test import Client
from django.urls import reverse
from django.test.html import parse_html, HTMLParseError


@pytest.mark.django_db
def test_root_index(client: Client):
    output = client.get(reverse("index"))
    assert (
        output.status_code == 200
    ), ("Index not reachable, %s" % output.reason_phrase)
    try:
        html = parse_html(output.getvalue().decode(output.charset))
    except HTMLParseError as e:
        raise AssertionError("%s%s%s" % ("Not valid HTML", os.sep, e))
    title = parse_html("<title>Holiday Homes</title>")
    assert (
        title in html
    ), "Invalid title of the index HTML page"
