from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import get_default_password_validators
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from .models import Article

res = get_default_password_validators()


class ArticleSerializerDetail(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["author"]


class ArticleSerializerList(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        exclude = ["content"]
        read_only_fields = [field.name for field in Article._meta.get_fields()]


User = get_user_model()


class UserRegisterRequestSerializer(serializers.ModelSerializer):
    is_subscription_requested = serializers.BooleanField(help_text="Do you want to see not public articles?",
                                                         label="Subscribe")

    def create(self, validated_data):
        is_subscription_requested = validated_data.pop("is_subscription_requested")
        user = User.objects.create_user(**validated_data)
        if is_subscription_requested:
            user.groups.add(Group.objects.get(name="subscribers"))
        return user

    def validate(self, data):
        user = User({key: val for key, val in data.items() if key != "is_subscription_requested"})
        errors = dict()
        try:
            validate_password(password=data.get('password'), user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

    class Meta:
        model = User
        fields = [User.USERNAME_FIELD, "password", "is_subscription_requested"]


class UserRegisterResultSerializer(serializers.HyperlinkedModelSerializer):
    is_subscriber = serializers.SerializerMethodField()

    def get_is_subscriber(self, instance):
        return instance.groups.filter(name="subscribers").count() > 0

    class Meta:
        model = User
        fields = ["url", "is_subscriber"]
