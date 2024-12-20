from django.apps import AppConfig


class MatriappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matriapp'

    def ready(self):
        import matriapp.signals  # Import signals to ensure they are registered