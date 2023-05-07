import pytest
import pathlib
from django.conf import settings


@pytest.fixture(scope='session')
def django_db_setup():
    BASE_DIR = pathlib.Path(__file__).parents[-3]
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str((BASE_DIR / 'oc-lettings-site.sqlite3').resolve()),
    }
