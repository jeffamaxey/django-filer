from django.urls import re_path

from . import settings as filer_settings
from . import views


urlpatterns = [
    re_path(
        f'{filer_settings.FILER_CANONICAL_URL}(?P<uploaded_at>[0-9]+)/(?P<file_id>[0-9]+)/$',
        views.canonical,
        name='canonical',
    )
]
