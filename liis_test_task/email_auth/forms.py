from django.contrib.auth.forms import UserChangeForm, UserCreationForm, UsernameField


class EmailInsteadUsernameUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("email",)
        field_classes = {"email": UsernameField}


class EmailAndUsernameSwappedUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ("email",)
        field_classes = {"email": UsernameField}
