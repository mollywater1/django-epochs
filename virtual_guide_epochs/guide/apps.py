from django.apps import AppConfig

class GuideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guide'

    def ready(self):
        import guide.signals  # Подключаем сигналы
