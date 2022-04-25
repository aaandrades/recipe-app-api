from django.contrib.auth import get_user_model, authenticate
# Extra languages supported by Django
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {
            'write_only': True,
            'min_length': 5}
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authentica the user"""
        email = attrs.get("email")
        password = attrs.get("password")

        # Access to the context of the request, which has all the
        # information about the request
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # If user doesnt exist, throw a new error
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        # If user exists, return the user
        attrs['user'] = user
        return attrs
