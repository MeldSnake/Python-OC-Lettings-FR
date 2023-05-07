import os
import pytest
from django.test import Client
from django.urls import reverse
from django.test.html import parse_html, HTMLParseError
from lettings.models import Letting


@pytest.mark.django_db
def test_lettings_index(client: Client):
    output = client.get(reverse("lettings:index"))
    assert (
        output.status_code == 200
    ), ("Index not reachable, %s" % output.reason_phrase)
    try:
        html = parse_html(output.getvalue().decode(output.charset))
    except HTMLParseError as e:
        raise AssertionError("%s%s%s" % ("Not valid HTML", os.sep, e))
    title = parse_html("<title>Lettings</title>")
    assert (
        title in html
    ), "Invalid title of the HTML page"


@pytest.mark.django_db
def test_lettings_object(client: Client):
    lettings = Letting.objects.all()
    for letting in lettings:
        title = letting.title
        output = client.get(reverse("lettings:letting", args=[letting.pk]))
        assert (
            output.status_code == 200
        ), ("Index not reachable, %s" % output.reason_phrase)
        try:
            html = parse_html(output.getvalue().decode(output.charset))
        except HTMLParseError as e:
            raise AssertionError("%s%s%s" % ("Not valid HTML", os.sep, e))
        # TODO See if needed to URLEncode the title
        title_elm = parse_html(f"<title>{title}</title>")
        assert (
            title_elm in html
        ), "Invalid title of the HTML page"
