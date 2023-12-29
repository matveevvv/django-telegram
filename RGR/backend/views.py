from django.shortcuts import render

from rest_framework import viewsets
from .models import Profile, Message,University
from .serializers import ProfileSerializer, MessageSerializer,UniversitySerializer
from django.views.decorators.csrf import csrf_exempt
from .localsettings import BOT_TOKEN
import requests
from django.http import HttpResponse 

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()    
    serializer_class = MessageSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer



def broadcast_message_view(request):
    return render(request, 'broadcast.html')

@csrf_exempt # данные, которые сервер отправляет браузеру в ожидании получить их обратно
def send_broadcast_message(request):
    if request.method == 'POST':                          # предназначен для направления запроса, при котором веб-сервер принимает данные, заключённые в тело сообщения, для хранения
        message = request.POST.get('message', '')  # получаем сообщение
        subscribers = Profile.objects.filter(subscription=True)
        bot_token = BOT_TOKEN 

        for subscriber in subscribers:
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            data = {'chat_id': subscriber.external_id, 'text': message}
            requests.post(url, data=data)

        return HttpResponse('Сообщение отправлено.')
    else:
        return HttpResponse('Ошибка', status=400)