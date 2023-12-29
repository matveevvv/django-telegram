
from django.contrib import admin
from .models import Profile, Message, University

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'name','residence','subscription')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'answer1', 'answer2','answer3', 'created_at')
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'specialization')