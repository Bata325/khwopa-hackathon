from django.db import models

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    violations = models.IntegerField(default=0)

    def __str__(self):
        return self.vehicle_number

    def increment_violations(self):
        self.violations += 1
        self.save()

    def send_sms(self, message):
        from twilio.rest import Client
        
        account_sid = "ACda8bf1e34f96c33c845738c7a8d8663d"
        auth_token = "6fecfb4510e49060fd81148221e2643b"
        twilio_number = "+17753735261"
        client = Client(account_sid, auth_token)

        try:
            client.messages.create(
                body=message,
                from_=twilio_number,
                to=self.phone_number
            )
            print(f"SMS sent to {self.vehicle_number}: {message}")
            self.increment_violations()
        except Exception as e:
            print(f"Failed to send SMS: {e}")