from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

urlpatterns += i18n_patterns(
    path("language/", set_language, name="language"),
    path("", include("common.urls")),
)

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
