import os
import sys

from django.apps import AppConfig
# from main1.services import start_scheduler


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main1'
    # start_scheduler()

    def ready(self):
        # if os.environ.get('RUN_MAIN') == 'True':
        if 'runserver' in sys.argv or 'manage' in sys.argv:
            from main1.services import start_scheduler
            start_scheduler()
