from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import UserSerializer, LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Allow registration and login without authentication
        """
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # Custom route for login
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    # Custom route for logout
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)

    # Get current user
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)