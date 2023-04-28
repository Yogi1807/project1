from django.contrib import admin  # noqa
from django.contrib.auth import get_user_model
from .models import Portal, JobDescription, JobTitle, Applicant

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#  TODO - refer -
#  https://docs.djangoproject.com/en/4.1/topics/i18n/translation/
# https://docs.djangoproject.com/en/4.1/topics/i18n/translation/#internationalization-in-python-code
#  Required to globalize our project
#  Required for translation
from django.utils.translation import gettext_lazy as _

# TODO
# refer
# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/actions/#adding-actions-to-the-modeladmin


# class UserAdmin(BaseUserAdmin):
#     ordering = ("email", )
#     list_display = ("email", "is_active")


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    ordering = ["id"]
    list_display = ["email", "name"]

    # TODO - reference
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Portal)
admin.site.register(JobTitle)
admin.site.register(JobDescription)
admin.site.register(Applicant)
