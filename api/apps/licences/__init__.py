from django.apps import AppConfig


class LicencesAppConfig(AppConfig):
    name = 'api.apps.licences'
    label = 'licences'
    verbose_name = 'Licences'

    def ready(self):
        import api.apps.licences.signals

default_app_config = 'api.apps.licences.LicencesAppConfig'