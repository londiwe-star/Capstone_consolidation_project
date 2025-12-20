"""
Django app configuration for the news application.
"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    Configuration class for the news application.
    
    This class handles app-level configuration including signal registration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        """
        Import signals when the app is ready.
        
        This method is called when Django starts up and ensures that
        signal handlers are registered for automated actions.
        """
        import news.signals
