from django.apps import AppConfig


class DevappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'devapp'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_crm_user, sender=self)

def _create_crm_user(sender, **kwargs):
    from django.contrib.auth.models import User
    from django.conf import settings

    username = settings.CRM_USERNAME
    password = settings.CRM_PASSWORD

    if not username or not password:
        return  # Silently skip if env vars are missing

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"is_staff": True, "is_superuser": True},
    )

    if created:
        user.set_password(password)
        user.save()
        print(f"[CRM] Admin user '{username}' created.")
    else:
        # Sync password if it changed in .env
        if not user.check_password(password):
            user.set_password(password)
            user.save()
            print(f"[CRM] Admin user '{username}' password updated.")
