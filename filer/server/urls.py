from django.urls import include, re_path

from .. import settings as filer_settings


urlpatterns = (
    []
    if filer_settings.FILER_0_8_COMPATIBILITY_MODE
    else [
        re_path(
            r'^'
            + filer_settings.FILER_PRIVATEMEDIA_STORAGE.base_url.lstrip('/'),
            include('filer.server.main_server_urls'),
        ),
        re_path(
            r'^'
            + filer_settings.FILER_PRIVATEMEDIA_THUMBNAIL_STORAGE.base_url.lstrip(
                '/'
            ),
            include('filer.server.thumbnails_server_urls'),
        ),
    ]
)
