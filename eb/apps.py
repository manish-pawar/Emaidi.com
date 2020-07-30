from django.apps import AppConfig


class EbConfig(AppConfig):
    name = 'eb'

    def ready(self):
        import eb.signals