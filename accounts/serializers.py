from django.core import validators

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

from .utils import validate_user_email, validate_password


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=7, max_length=16, write_only=True)
    re_password = serializers.CharField(min_length=7, max_length=16, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 're_password']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(
                {'message': 'Veillez entrer une adresse email'}
            )


        return value

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            validate_user_email(email)
        except Exception as e:
            raise serializers.ValidationError(
                {
                    'message': 'Adresse email non valid',
                    'details': str(e)
                }
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'message': 'Cette adresse est déja utilisée'}
            )

        password = attrs.get('password', '')
        re_password = attrs.get('re_password', '')

        if not password and re_password:
            raise serializers.ValidationError(
                {'message': 'Le mot de pass est obligatoire'}
            )
        else:
            validate_password(password)
            if password != re_password:
                raise serializers.ValidationError(
                    {'message': 'Les mots de passe sont obligatoire'}
                )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class AccountActivationSerializer(serializers.Serializer):
    otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=7, max_length=16, write_only=True)
    new_password = serializers.CharField(min_length=7, max_length=16, write_only=True)
    confirm_new_password = serializers.CharField(min_length=7, max_length=16, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Le mot de pass ancient n\'est pas correcte'})

        try:
            validate_password(new_password)
        except Exception as e:
            raise serializers.ValidationError(
                {
                    'message': 'Mot de pass trop faible',
                    'details': str(e),
                }
            )

        if old_password == new_password:
            raise serializers.ValidationError({'new_password': 'Le nouveau mot de pass doit ètre different du precedant'})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({'new_password': 'Les mots de pass ne corespondent pas'})

        return attrs



class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=7, max_length=16, write_only=True)
    confirm_new_password = serializers.CharField(min_length=7, max_length=16, write_only=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(
                {'message': 'L\'email est requis'}
            )

        try:
            validators.validate_email(value)
        except Exception as e:
            raise serializers.ValidationError(
                {
                    'message': 'Adresse email invalid',
                    'details': str(e)
                }
            )
        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        try:
            validate_password(new_password)
        except Exception as e:
            raise serializers.ValidationError(
                {
                    'message': 'Password to weak',
                    'details': str(e),
                }
            )
        if new_password != confirm_new_password:
            raise serializers.ValidationError({'message': 'Les mots de pass ne corespondent pas'})
        return attrs



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_online', 'is_active', 'joined_at', 'last_login']



class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        return token
