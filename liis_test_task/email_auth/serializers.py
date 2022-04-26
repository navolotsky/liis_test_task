from django.contrib.auth import get_user_model

from rest_framework import serializers, validators

User = get_user_model()

User = get_user_model()
username_field_name = "username"
username_field = User._meta.get_field(username_field_name)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
        required=False, allow_blank=False, allow_null=True, default=None,
        max_length=username_field.max_length,
        validators=[User.username_validator, validators.UniqueValidator(User.objects.all())],
        help_text=username_field.help_text,
        error_messages=username_field.error_messages)

    class Meta:
        model = User
        fields = ["url", "email", "username", "first_name", "last_name", "is_staff", "last_login"]
        read_only_fields = ["last_login"]
