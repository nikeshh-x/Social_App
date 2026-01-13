from django.apps import AppConfig


class AUsersConfig(AppConfig):
    name = 'a_users'

    def ready(self):
        import a_users.signals
