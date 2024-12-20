# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignupForm, ProfileForm, PartnerPreferenceForm, MessageForm, EventForm
from .models import Profile, PartnerPreference, User, Message, Event, EventResponse
from django.utils import timezone
from .utils import calculate_match_score

# Welcome Page for Signup
def welcome(request):
    return signup(request)  # Redirect to signup view for consistency

# User Signup View
def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')

            # Check if user already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "Username or email already exists.")
                return redirect('signup')

            user = user_form.save()  # Save the new user
            django_login(request, user)  # Log in the user after registration
            
            return redirect('create_profile')  # Redirect to profile creation page

    else:
        user_form = SignupForm()

    return render(request, 'matriapp/signup.html', {'user_form': user_form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Use data parameter for AuthenticationForm
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)  # Log in the user
            return redirect('home')  # Redirect to home after logging in
        else:
            messages.error(request, "Invalid username or password.")  # Show error message for invalid login.
    else:
        form = AuthenticationForm()  # Create an empty authentication form
    
    return render(request, 'matriapp/login.html', {'form': form})

# Profile Creation View - Require Login
@login_required  # Ensure only logged-in users can access this view
def create_profile(request):
    profile_instance, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if profile_form.is_valid():
            profile_form.save()  # Save the updated or newly created profile
            messages.success(request, "Your profile has been created!")  # Success message
            return redirect('partner_preference')  # Redirect to partner preference page
    else:
        profile_form = ProfileForm(instance=profile_instance)

    return render(request, 'matriapp/create_profile.html', {'profile_form': profile_form})

# User Profile View for Editing Existing Profiles - Require Login
@login_required  # Ensure only logged-in users can access this view
def profile(request):
    profile_instance = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()  # Save the updated profile
            messages.success(request, "Your profile has been updated!")  # Success message
            return redirect('home')  # Redirect to home after saving
    else:
        form = ProfileForm(instance=profile_instance)

    return render(request, 'matriapp/profile.html', {'form': form})

# Partner Preference View - Require Login
@login_required  # Ensure only logged-in users can access this view
def partner_preference(request):
    if request.method == 'POST':
        partner_preference_form = PartnerPreferenceForm(request.POST)
        if partner_preference_form.is_valid():
            partner_preference = partner_preference_form.save(commit=False)
            partner_preference.user = request.user  # Associate with logged-in user
            partner_preference.save()
            messages.success(request, "Your partner preferences have been saved!")  # Success message
            return redirect('home')  # Redirect to home after completing preferences
    else:
        partner_preference_form = PartnerPreferenceForm()

    return render(request, 'matriapp/partner_preference.html', {'partner_preference_form': partner_preference_form})

# Home View - Require Login and include additional context data
@login_required  # Ensure only logged-in users can access this view
def home(request):
    upcoming_events = Event.objects.filter(participants=request.user, event_datetime__gte=timezone.now()).order_by('event_datetime')
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False)

    try:
        partner_preference = PartnerPreference.objects.get(user=request.user)
    except PartnerPreference.DoesNotExist:
        partner_preference = None

    context = {
        'upcoming_events': upcoming_events,
        'unread_messages': unread_messages,
        'partner_preference': partner_preference,
    }
    
    return render(request, 'matriapp/home.html', context)

# Matches View for Finding Potential Matches - Require Login
@login_required  
def matches(request):
    user_matches_list = []  
    potential_matches = User.objects.exclude(id=request.user.id)  
    
    for potential_match in potential_matches:
        try:
            score = calculate_match_score(request.user, potential_match)  
            if score > 0:  
                user_matches_list.append({'user': potential_match, 'score': score})  
        except PartnerPreference.DoesNotExist:
            continue
    
    user_matches_list.sort(key=lambda x: x['score'], reverse=True)  
    
    return render(request, 'matriapp/matches.html', {'matches': user_matches_list})

# Messages View for Viewing User Messages - Require Login 
@login_required
def messages_view(request):  
    user_messages_list = Message.objects.filter(receiver=request.user)  

    if request.method == 'POST':
        message_form = MessageForm(request.POST, user=request.user)  # Pass current user
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.sender = request.user  # Set sender as the logged-in user
            new_message.save()
            return redirect('messages_view')  # Redirect to the same page after sending

    else:
        message_form = MessageForm(user=request.user)  # Pass current user

    return render(request, 'matriapp/messages.html', {
        'messages': user_messages_list,
        'message_form': message_form,
    })

# Create Event View - Require Login 
@login_required  
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            notify_partner(event)  # Notify partner about the event (make sure this function is defined)
            messages.success(request, "Your event has been created!")  # Success message
            return redirect('events_view')
    else:
        form = EventForm()
    
    return render(request, 'matriapp/create_event.html', {'form': form})

# Respond to Event View - Require Login 
@login_required  
def respond_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        response = request.POST.get('response') == 'accept'
        EventResponse.objects.update_or_create(
            event=event,
            user=request.user,
            defaults={'response': response}
        )
        
        messages.success(request, "Your response has been recorded!")  # Success message
        return redirect('events_view')

# Events View for Viewing User Events - Require Login 
@login_required  
def events_view(request):  
    user_events_list = Event.objects.filter(participants=request.user)  
    return render(request,'matriapp/events.html',{'events':user_events_list})  

# Available Profiles View - Require Login 
@login_required  
def available_profiles(request):
    opposite_gender_profiles = Profile.objects.filter(gender='Female' if request.user.profile.gender == 'Male' else 'Male')
    
    return render(request, 'matriapp/available_profiles.html', {'profiles': opposite_gender_profiles})

# Mark as Read Functionality - Require Login 
@login_required  
def mark_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id, receiver=request.user)
        message.is_read = True
        message.save()
        messages.success(request, "Message marked as read.")  # Success message
        return redirect('messages_view')
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
        return redirect('messages_view')

# Chat Room View for Real-Time Chat Functionality - Require Login 
@login_required  
def chat_room(request, room_name):
    return render(request,'matriapp/chat_room.html',{'room_name': room_name})  