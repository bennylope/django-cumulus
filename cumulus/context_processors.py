from django.conf import settings

from cumulus.storage import CloudFilesStorage
from cumulus.settings import CUMULUS


def cdn_url(request):
    """
    A context processor to expose the full cdn url in templates.

    """
    static_container = CUMULUS.get('STATIC_CONTAINER', None)
    cloudfiles_storage = CloudFilesStorage(container=static_container)
    static_url = settings.STATIC_URL
    container_url = cloudfiles_storage._get_container_url()
    cdn_url = container_url + static_url

    return {'CDN_URL': cdn_url}


def static_cdn_url(request):
    """
    Context processor that switches between full CDN URL in templates and a
    locally definined static media URL. Ideal for local development.

    Defaults to the opposite of the project's DEBUG status.
    """
    use_cdn = CUMULUS.get('USE_CDN_STATIC', not(settings.DEBUG))
    if use_cdn:
        url = cdn_url(request)['CDN_URL']
    else:
        url = settings.STATIC_URL
    return {'STATIC_URL': url}
