#Users.views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth  import login, logout
from rest_framework.authentication import SessionAuthentication
from .models import User
from .serializers import UserSerializer, LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
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

        login(request, user)

        response = Response({
            'message':'Login successful',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='sessionid',
            value=request.session.session_key,
            httponly=True,
            samesite='None',
            secure=False
        )
        return response
        

    # Custom route for logout
    @action(detail=False, methods=['post'], url_path='logout')
    def logout_user(self, request):
        logout(request)
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('sessionid')
        return response

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)