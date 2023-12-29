from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, MessageViewSet,UniversityViewSet,broadcast_message_view,send_broadcast_message

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet,basename='profile')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'universities', UniversityViewSet, basename='university')

urlpatterns = [
    path('', include(router.urls)),
    path('send-broadcast/', send_broadcast_message, name='send_broadcast'),
    path('message/', broadcast_message_view, name='broadcast_message'),
]
