from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from api.serializers import UserSerializer

User = get_user_model()


@extend_schema(
    request=inline_serializer('RegisterRequest', fields={
        'email': serializers.EmailField(),
        'password': serializers.CharField(),
        'role': serializers.ChoiceField(choices=['FARMER', 'BUYER']),
        'first_name': serializers.CharField(required=False),
        'last_name': serializers.CharField(required=False),
    }),
    responses={201: UserSerializer},
    tags=['Auth']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'BUYER')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        role=role,
        first_name=first_name,
        last_name=last_name,
    )

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)},
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    request=inline_serializer('LoginRequest', fields={
        'email': serializers.EmailField(),
        'password': serializers.CharField(),
    }),
    responses={200: UserSerializer},
    tags=['Auth']
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    login_val = request.data.get('email')  # email ya username dono
    password = request.data.get('password')

    if not login_val or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    try:
        user = User.objects.get(email=login_val)
    except User.DoesNotExist:
        try:
            user = User.objects.get(username=login_val)
        except User.DoesNotExist:
            pass

    if not user or not user.check_password(password):
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)},
    })


@extend_schema(
    request=inline_serializer('LogoutRequest', fields={
        'refresh': serializers.CharField(),
    }),
    responses={200: None},
    tags=['Auth']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'message': 'Logged out successfully.'})
    except Exception:
        return Response({'error': 'Invalid or missing refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer},
    tags=['Auth']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response(UserSerializer(request.user).data)