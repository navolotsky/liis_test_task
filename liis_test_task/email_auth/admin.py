from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import EmailAndUsernameSwappedUserChangeForm, EmailInsteadUsernameUserCreationForm
from .models import User


def swap_username_and_email(fieldsets):
    result = deepcopy(fieldsets)
    for _, params in result:
        params["fields"] = tuple(
            name if name not in ("username", "email")
            else ("email" if name == "username" else "username")
            for name in params["fields"]
        )
    return result


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = EmailAndUsernameSwappedUserChangeForm
    add_form = EmailInsteadUsernameUserCreationForm
    ordering = ("pk",)
    fieldsets = swap_username_and_email(BaseUserAdmin.fieldsets)
    add_fieldsets = swap_username_and_email(BaseUserAdmin.add_fieldsets)
    list_display = ("email", "first_name", "last_name", "username", "is_staff")
