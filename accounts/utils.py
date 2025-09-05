import os
import logging
import re
import string
import random
from datetime import datetime

from smtplib import SMTPException

from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError

from rest_framework import serializers

from accounts.models import User


logger = logging.getLogger(__name__)

site_name = os.getenv('SITE_NAME')


def generate_otp(length=5):
    digits = string.digits
    chars = string.ascii_uppercase

    otp = ''.join(random.choice(digits + chars) for _ in range(length))
    print("otp created..................")
    return otp


def send_otp(email):

    try:
        otp_code = generate_otp()
        user = User.objects.filter(email=email).first()
        if user is None:
            logger.error('User not found.')
        user.otp = otp_code
        subject = 'One Time Password For Email Verification.'
        html_message = render_to_string('accounts/activation_code.html', {'site_name': site_name, 'otp': otp_code, 'year': datetime.now().year})
        print('OTP code sent...')
        email_message = EmailMessage(subject=subject, body=html_message, from_email='sadeckbt@gmail.com', to=[email])
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
        user.save()
        logger.info(f'Email sent successfully to {email}')

    except BadHeaderError:
        logger.error(f"Invalid header found when sending email to {email}")
    except SMTPException as e:
        logger.error(f"SMTP error occurred when sending email to {email}: {e}")
    except Exception as e:
        logger.error(f"An error occurred when sending email to {email}: {e}")



def send_reset_password_otp(email):
    try:
        otp_code = generate_otp()
        user = User.objects.filter(email=email).first()
        if user is None:
            logger.error('User not found.')
        user.otp = otp_code
        subject = 'One Time Password Code To Reset Account Password.'
        html_message = render_to_string('accounts/reset_password_code.html', {'otp': otp_code})
        print('OTP code sent...')
        email_message = EmailMessage(subject=subject, body=html_message, from_email='sadeckbt@gmail.com', to=[email])
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
        user.save()
        logger.info(f'Email sent successfully to {email}')

    except BadHeaderError:
        logger.error(f"Invalid header found when sending email to {email}")
    except SMTPException as e:
        logger.error(f"SMTP error occurred when sending email to {email}: {e}")
    except Exception as e:
        logger.error(f"An error occurred when sending email to {email}: {e}")


def validate_user_email(email):
    try:
        validate_email(email)
    except Exception as e:
        raise serializers.ValidationError(
            {
                'message': 'Invalid email address',
                'details': str(e)
            }
        )


def validate_password(password):
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if len(password) < 7:
        return False
    return True
