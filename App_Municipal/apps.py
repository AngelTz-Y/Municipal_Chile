from django.apps import AppConfig

class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Municipal'

    def ready(self):
        import App_Municipal.signals  # Importa las señales para que se ejecuten
