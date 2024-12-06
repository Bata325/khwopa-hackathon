from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Vehicle
from twilio.rest import Client

# Unregister default User and Group models
admin.site.unregister(User)
admin.site.unregister(Group)

# Twilio configuration
TWILIO_ACCOUNT_SID = "ACda8bf1e34f96c33c845738c7a8d8663d"
TWILIO_AUTH_TOKEN = "6fecfb4510e49060fd81148221e2643b"
TWILIO_PHONE_NUMBER = "+17753735261"

# Custom admin action to send SMS
def send_sms_action(modeladmin, request, queryset):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for vehicle in queryset:
        try:
            message = client.messages.create(
                body=f"Hello, this is a message for vehicle {vehicle.vehicle_number}.",
                from_=TWILIO_PHONE_NUMBER,
                to=vehicle.phone_number,
            )
            modeladmin.message_user(request, f"SMS sent to {vehicle.vehicle_number}: {vehicle.phone_number}")
        except Exception as e:
            modeladmin.message_user(request, f"Failed to send SMS to {vehicle.vehicle_number}: {str(e)}", level="error")

send_sms_action.short_description = "Send SMS to selected vehicles"

# Vehicle admin configuration
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'phone_number', 'violations')
    search_fields = ('vehicle_number', 'phone_number')
    actions = [send_sms_action]  # Add the custom action

# Register Vehicle model
admin.site.register(Vehicle, VehicleAdmin)