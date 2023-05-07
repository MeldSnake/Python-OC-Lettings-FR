import os
import pytest
from django.test import Client
from django.urls import reverse
from django.test.html import parse_html, HTMLParseError
from profiles.models import Profile


@pytest.mark.django_db
def test_profiles_index(client: Client):
    output = client.get(reverse("profiles:index"))
    assert (
        output.status_code == 200
    ), ("Index not reachable, %s" % output.reason_phrase)
    try:
        html = parse_html(output.getvalue().decode(output.charset))
    except HTMLParseError as e:
        raise AssertionError("%s%s%s" % ("Not valid HTML", os.sep, e))
    title = parse_html("<title>Profiles</title>")
    assert (
        title in html
    ), "Invalid title of the HTML page"


@pytest.mark.django_db
def test_profiles_object(client: Client):
    profiles = Profile.objects.all()
    for profile in profiles:
        title = profile.user.username
        output = client.get(reverse("profiles:profile", args=[profile.user.username]))
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
