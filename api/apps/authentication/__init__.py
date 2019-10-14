from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'api.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import api.apps.authentication.signals


default_app_config = 'api.apps.authentication.AuthenticationAppConfig'