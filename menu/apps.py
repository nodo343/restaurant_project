from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'
    verbose_name = 'რესტორნის მენიუ'

    def ready(self):
        from django import VERSION as DJANGO_VERSION

        if DJANGO_VERSION >= (5, 2, 8):
            return

        from django.template.context import BaseContext

        def copy_context(context):
            duplicate = context.__class__.__new__(context.__class__)
            duplicate.__dict__.update(context.__dict__)
            duplicate.dicts = context.dicts[:]
            return duplicate

        BaseContext.__copy__ = copy_context
