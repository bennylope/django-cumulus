django-cumulus
==============

The aim of django-cumulus is to provide a set of tools to utilize Rackspace Cloud Files through Django. It currently includes a custom file storage class, CloudFilesStorage.

.. toctree::
   :maxdepth: 2
   :hidden:

   changelog

.. comment: split here

Installation
************

To install the latest release (currently 1.0.3) from PyPI using pip::

    pip install django-cumulus

To install the development version using pip::

    pip install -e git://github.com/richleland/django-cumulus.git#egg=django-cumulus

Add ``cumulus`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'cumulus',
        ...
    )

Usage
*****

Add the following to your project's settings.py file::

    CUMULUS_USERNAME = 'YourUsername'
    CUMULUS_API_KEY = 'YourAPIKey'
    CUMULUS_CONTAINER = 'ContainerName'
    DEFAULT_FILE_STORAGE = 'cumulus.storage.CloudFilesStorage'

Alternatively, if you don't want to set the DEFAULT_FILE_STORAGE, you can do the following in your models::

    from cumulus.storage import CloudFilesStorage

    cloudfiles_storage = CloudFilesStorage()

    class Photo(models.Model):
        image = models.ImageField(storage=cloudfiles_storage, upload_to='photos')
        alt_text = models.CharField(max_length=255)

Then access your files as you normally would through templates::

    <img src="{{ photo.image.url }}" alt="{{ photo.alt_text }}" />

Or through Django's default ImageField or FileField api::

    >>> photo = Photo.objects.get(pk=1)
    >>> photo.image.width
    300
    >>> photo.image.height
    150
    >>> photo.image.url
    http://c0000000.cdn.cloudfiles.rackspacecloud.com/photos/some-image.jpg

Management command
******************

django-cumulus ships with a management command for synchronizing a local static media folder with a remote container. A few extra settings are required to make use of the command.

Add the following required settings::

     # the name of the container to sync with
    CUMULUS_STATIC_CONTAINER = 'MyStaticContainer'

    # whether to use rackspace's internal private network
    CUMULUS_USE_SERVICENET = False

    # a list of files to exclude from sync
    CUMULUS_FILTER_LIST = []

Invoke the management command::

    ./manage.py syncstatic

You can also perform a test run::

    ./manage.py syncstatic -t

For a full list of available options::

    ./manage.py help syncstatic

Context Processors
******************

django-cumulus includes two optional context processors for accessing the URLs of CDN hosted files from your templates. The ``cdn_url`` context processor 

Explicit CDN path variable
--------------------------

The ``cdn_url`` context processor adds the full URL to your CDN host to the context allowing you to access the full CDN_URL of any container files from your templates.

This is useful when you're using Cloud Files to serve static media such as CSS and JavaScript and don't have access to the ``ImageField`` or ``FileField``'s url() convenience method.

Add ``cumulus.context_processors.cdn_url`` to the list of context processors in your project's settings.py file::


    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'cumulus.context_processors.cdn_url',
        ...
    )

Now in your templates you can use {{ CDN_URL }} to output the full path to local media::

    <link rel="stylesheet" href="{{ CDN_URL }}css/style.css">

STATIC_URL context variable
---------------------------

The ``static_cdn_url`` context processor is handy if you are using ``django.contrib.staticfiles`` or its predecessor ``django-staticfiles`` in conjunction with django-cumulus ``syncstatic``. It's also helpful if you primarily use a CDN for production static media files but don't want to access (or can't access) the CDN while developing.

The context processor conditionally updates the STATIC_URL context variable used by staticfiles (``django.contrib.staticfiles`` or ``django-staticfiles``) with the full CDN path *or* the standard static media based on your project settings.

Add ``cumulus.context_processors.cdn_url`` to the list of context processors in your project's settings.py file::


    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'cumulus.context_processors.static_cdn_url',
        ...
    )

The context processor will default to providing full CDN URLs if ``settings.DEBUG`` is ``False``. If ``settings.DEBUG`` is ``True`` then the context processor will pass the STATIC_URL variable as provided by the staticmedia application without any modification.

You can override this conditional functionality by explicitly toggling the ``USE_CDN_STATIC`` value in the CUMULUS settings dictionary::

    CUMULUS = {
        ...
        'USE_CDN_STATIC': True,
        ...
    }

You can reference static media over the CDN as you would normally::

    <link rel="stylesheet" href="{{ STATIC_URL }}css/style.css">

Result with ``USE_CDN_STATIC`` set to ``True``::

    <link rel="stylesheet" href="http://public.container.url.rackcdn.com/static_directory/css/style.css">

Result with ``USE_CDN_STATIC`` set to ``False``::

    <link rel="stylesheet" href="/static_url/css/style.css">

Requirements
************

* Django >= 1.1.4
* python-cloudfiles >= 1.7.8

Tests
*****

To run the tests, add ``cumulus`` to your ``INSTALLED_APPS`` and run::

    django-admin.py test cumulus

This will upload two very small files to your container and delete them when the tests have finished running.

Issues
******

To report issues, please use the issue tracker at https://github.com/richleland/django-cumulus/issues.
