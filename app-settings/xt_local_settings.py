# -*- coding: utf-8 -*-


def configure(settings):
    settings.DEBUG = True 

    settings.DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

    # xwrap config
    settings.XWRAP_URL = "http://127.0.0.1:8999/api"
    settings.XWRAP_SKIP_TEST = True

    settings.INSTALLED_APPS = settings.INSTALLED_APPS + (
        'django_extensions',
    )

#    for _, database_settings in settings.DATABASES.items():
#        database_settings['ENGINE'] = 'django.db.backends.sqlite3'
#        database_settings['NAME'] = '/Users/yorrick/tests/test_db_sqlite3'

    for _, database_settings in settings.DATABASES.items():
        database_settings['USER'] = 'dev'
#        database_settings['USER'] = 'voiturolio'
        database_settings['PASSWORD'] = 'dev'
#        database_settings['PASSWORD'] = 'voiturolio'
        database_settings['HOST'] = 'localhost'
#        database_settings['HOST'] = '192.168.1.66'
        database_settings['PORT'] = '5432'

    settings.LOGGING['handlers']['console']['formatter'] = 'simple'
    settings.LOGGING['loggers'].pop('xt')
    
#    settings.LOGGING['loggers']['xt.business_hours'] = {'handlers': ['console'], 'level': 'WARN'}
#    settings.LOGGING['loggers']['xt.newcars'] = {'handlers': ['console'], 'level': 'DEBUG'}
    settings.LOGGING['loggers']['xt.promos_make'] = {'handlers': ['console'], 'level': 'DEBUG'}
    settings.LOGGING['loggers']['xt.xforms'] = {'handlers': ['console'], 'level': 'DEBUG'}
    settings.LOGGING['loggers']['ttr.t_cms.views.promotions'] = {'handlers': ['console'], 'level': 'DEBUG'}
    
#    settings.LOGGING['loggers']['xt.business_hours'] = {'handlers': ['console'], 'level': 'DEBUG'}

    settings.CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '',
    }

#    settings.CACHES['default'] = {
#            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#            'LOCATION': 'localhost:11211',
#            'OPTIONS': {
#                'tcp_nodelay': True,
#                'hash': 'fnv1a_64',
#                'distribution': 'consistent ketama',
#            },
#        }

