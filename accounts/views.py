from datetime import datetime

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User
from .serializers import UserSerializer, RegistrationSerializer, AccountActivationSerializer, LoginSerializer, \
    ChangePasswordSerializer, ResetPasswordSerializer
from .utils import send_otp, send_reset_password_otp


# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        serializer = RegistrationSerializer(user)
        send_otp(user.email)
        return Response(
            {
                'message': f'Votre compte a été crée, verifier vos mails ({user.email}), pour l\'activer',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {
            'message': 'Données non valid',
            'details': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def account_activation(request):
    serializer = AccountActivationSerializer(data=request.data)
    if serializer.is_valid():
        otp = serializer.data['otp']
        user = User.objects.filter(otp=otp).first()
        user_instance = RegistrationSerializer(user).data
        if not user:
            return Response(
                {
                    'success': False,
                    'message': 'Otp non valid',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.is_online = True
        user.otp = None
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'success': True,
                'message': 'Compte activé',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'exp': datetime.fromtimestamp(refresh.access_token['exp']).isoformat(),
                'data': user_instance
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            'success': False,
            'message': 'Données non valids',
            'details': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    user = request.user
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response(
            {
                'success': False,
                'details': 'Refresh token is required',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)

        # Blacklist the token
        token.blacklist()
        if not user.is_admin:
            request.user.is_online = False
        user.save()

        return Response(
            {
                'success': True,
                'message': 'Deconnecté',
            },
            status=status.HTTP_205_RESET_CONTENT
        )
    except TokenError as e:
        return Response(
            {
                'message': '',
                'details': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid email or password',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        user.is_online = True
        user.save()
        user_instance = RegistrationSerializer(user).data

        return Response(
            {
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'exp': datetime.fromtimestamp(refresh.access_token['exp']).isoformat(),
                'data': user_instance
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            'success': False,
            'message': 'Invalid data',
            'details': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        new_password = serializer.validated_data.get('new_password')
        confirm_new_password = serializer.validated_data.get('confirm_new_password')

        try:
            user = request.user
            if new_password != confirm_new_password:
                return Response(
                    {
                        'success': False,
                        'message': 'Passwords do not match',
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {
                    'success': True,
                    'message': 'Password changed',
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Something turn wrong, try again',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        {
            'success': False,
            'message': 'Invalid data',
            'details': serializer.errors
        }
    )


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()

    if user:
        send_reset_password_otp(user.email)
    return Response(
            {
                'success': True,
                'message': f'Otp sent to {user.email}'
            },
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')
        new_password = serializer.validated_data.get('new_password')
        try:
            user = User.objects.filter(email=email, otp=otp).first()

            if not user:
                return Response(
                    {
                        'success': False,
                        'message': 'Wrong otp or otp expired'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            user.set_password(new_password)
            user.otp = None
            user.save()

            return Response(
                {
                    'success': True,
                    'message': 'Password changed'
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'Something turn wrong, try again',
                    'details': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        {
            'success': False,
            'message':'Invalid data',
            'details': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    password = request.data.get('password')
    try:
        user = request.user
        if user.check_password(password):
            user.delete()
            return Response(
                {
                    'success': True,
                    'message': 'Account deleted'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {
                'success': False,
                'message': 'Invalid password'
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                'success': False,
                'message': 'Something turn wrong, try again',
                'details': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request):
    user = request.user
    return Response(
        UserSerializer(user).data,
        status=status.HTTP_200_OK
    )



#RefreshObtainSerializer
@api_view(["POST"])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh_token')
        refresh = RefreshToken(refresh_token)
        return Response(
            {
                "refresh ": str(refresh),
                "access": str(refresh.access_token),
                "date_exp": refresh.access_token["exp"],
            }
        )
    except TokenError as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
