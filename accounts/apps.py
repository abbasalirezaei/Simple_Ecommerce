from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'



    name = 'accounts'  # The name of the app
    icon = 'fa fa-user'  # FontAwesome icon for the app (optional)
    divider_title = "Accounting "  # Title of the section divider in the sidebar (optional)
    priority = 4  # Determines the order of the app in the sidebar (higher values appear first, optional)
    hide = False  # Set to True to hide the app from the sidebar menu (optional)
    def ready(self):
        import accounts.signals