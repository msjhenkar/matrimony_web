# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, PartnerPreference, User, Message, Event

class SignupForm(UserCreationForm):  
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'gender', 
                  'religion', 'caste', 'height', 
                  'education', 'occupation', 
                  'income', 'profile_picture']

class PartnerPreferenceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreference
        fields = ['min_age', 'max_age', 
                  'min_height', 'max_height',
                  'religion', 'caste',
                  'education', 'occupation',
                  'location']
class MessageForm(forms.ModelForm):
    sender = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Initially empty; will populate in __init__
        required=True,
        label="Sender"
    )
    
    receiver = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Initially empty; will populate in __init__
        required=True,
        label="Receiver"
    )

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content']  # Include sender and receiver in the fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the current user from kwargs
        super(MessageForm, self).__init__(*args, **kwargs)

        # Populate sender dropdown with current user (optional)
        self.fields['sender'].queryset = User.objects.filter(id=user.id)

        # Populate receiver dropdown with users of the opposite gender
        if user.profile.gender == 'Male':
            self.fields['receiver'].queryset = User.objects.filter(profile__gender='Female')
        else:
            self.fields['receiver'].queryset = User.objects.filter(profile__gender='Male')



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_datetime']  # Use event_datetime instead of separate date and time
        # admin.py



