# urls.py

from django.urls import path
from .views import (
    welcome,
    signup,
    login_view,
    create_profile,
    partner_preference,
    profile,
    home,
    matches,
    messages_view,
    chat_room,
    events_view,
    mark_as_read,
    available_profiles,
    create_event,
)

urlpatterns = [
    path('', welcome, name='welcome'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('create_profile/', create_profile, name='create_profile'),
    path('partner_preference/', partner_preference, name='partner_preference'),
    path('profile/', profile, name='profile'),
    path('home/', home, name='home'),
    path('matches/', matches, name='matches'),
    
    # New URLs
    path('messages/', messages_view, name='messages_view'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
    path('events/', events_view, name='events_view'),
    
    path('mark_as_read/<int:message_id>/', mark_as_read, name='mark_as_read'),
    path('available_profiles/', available_profiles, name='available_profiles'),
    # matriapp/urls.py

    path('create_event/', create_event, name='create_event'),  # Ensure this line exists
    # Add other URL patterns as needed
]
