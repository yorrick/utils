# -*- coding: utf-8 -*-

def configure(settings):
    settings.DEBUG = False

    settings.DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

    # xwrap config
    settings.XWRAP_URL = "http://127.0.0.1:8999/api"

    for _, database_settings in settings.DATABASES.items():
        database_settings['USER'] = 'dev'
        database_settings['PASSWORD'] = 'dev2005ak'
        database_settings['HOST'] = 'localhost'
        database_settings['PORT'] = '5432'

    settings.LOGGING['loggers']['xt.business_hours'] = {'handlers': ['console'], 'level': 'WARN'}
    settings.LOGGING['loggers']['xt.newcars'] = {'handlers': ['console'], 'level': 'DEBUG'}

#    settings.CACHES['default'] = {
#            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#            'LOCATION': 'localhost:11211',
#            'OPTIONS': {  
#                'tcp_nodelay': True,
#                'hash': 'fnv1a_64',
#                'distribution': 'consistent ketama',
#            },
#        }
