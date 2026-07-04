from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings

def generate_email_token():
    return str(uuid4())

def send_verification_email(email, token):
    subject = "Verify your email"
    message = f"Please verify your email by clicking the following link: http://127.0.0.1:8000/api/auth/verify-email/{token}/"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
)
