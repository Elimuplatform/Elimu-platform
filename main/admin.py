from django.contrib import admin
from django.utils.html import format_html
from .models import FounderInfo, Notice, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Inatengeneza cSafu za kuonyesha Jina, Email, Simu, na Picha
    list_display = ('get_username', 'get_email', 'phone_number', 'display_passport')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Jina la Mtumiaji'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Barua Pepe'

    # Kitendo cha kuonyesha picha ndogo kwenye orodha ya Admin
    def display_passport(self, obj):
        if obj.passport_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.passport_photo.url)
        return "Hakuna Picha"
    display_passport.short_description = 'Passport'

admin.site.register(FounderInfo)
admin.site.register(Notice)