from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from managerApp.models import Task
from .serializers import TaskSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdminOrAssignedUser
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Task.objects.all()
        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        if self.request.user.is_admin() and 'assigned_to' in self.request.data:
            serializer.save()
        else:
            serializer.save(assigned_to=self.request.user)

    def perform_update(self, serializer):
        task = self.get_object()
        if serializer.validated_data.get('status') == Task.Status.COMPLETED and not task.completed_date:
            serializer.save(completed_date=timezone.now())
        else:
            serializer.save()
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)