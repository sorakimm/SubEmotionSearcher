from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'searchsite'

    def ready(self):
        import searchsite.search.signals
