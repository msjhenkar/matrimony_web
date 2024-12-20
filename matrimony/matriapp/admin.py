from django.contrib import admin
from .models import User, Profile, PartnerPreference, Match, Message, Event

class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 1  # Allows adding one additional profile inline

class PartnerPreferenceInline(admin.StackedInline):
    model = PartnerPreference
    extra = 1  # Allows adding one additional partner preference inline

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified')
    search_fields = ('username', 'email')
    inlines = [ProfileInline, PartnerPreferenceInline]  # Add inlines for profile and partner preference

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date', 'gender')
    search_fields = ('user__username', 'location')

class PartnerPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'min_age', 'max_age', 'religion')
    search_fields = ('user__username', 'religion')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('user', 'matched_user', 'match_score', 'created_at')
    search_fields = ('user__username', 'matched_user__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('sender__username', 'receiver__username')

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_datetime', 'created_by')  # Use event_datetime instead of date
    search_fields = ('title', 'location', 'created_by__username')

# Register the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PartnerPreference, PartnerPreferenceAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Event, EventAdmin)  # Ensure this line is present only once