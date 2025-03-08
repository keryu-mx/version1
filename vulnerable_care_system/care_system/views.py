from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Subject, Custodian, Alarm
from .serializers import SubjectSerializer, CustodianSerializer, AlarmSerializer
from twilio.rest import Client
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_alarm_via_qr_code_api(request):
    """
    Trigger an alarm using QR code data.
    """
    qr_code_data = request.data.get('qr_code_data')
    if not qr_code_data:
        return Response({"error": "QR code data is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Extract subject_id from QR code data (e.g., "subject_id:1")
        subject_id = int(qr_code_data.split(':')[1])
        subject = Subject.objects.get(id=subject_id)

        # Create a new alarm for the subject
        alarm = Alarm.objects.create(subject=subject)

        # Notify custodians (optional, if you have WhatsApp integration)
        # Example: send_whatsapp_message(subject.custodians, "An alarm has been triggered!")

        return Response({"message": "Alarm triggered successfully", "alarm_id": alarm.id}, status=status.HTTP_201_CREATED)

    except (IndexError, ValueError, Subject.DoesNotExist):
        return Response({"error": "Invalid QR code data or subject not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_qr_code_api(request, subject_id):
    """
    Retrieve the QR code for a specific subject.
    """
    try:
        subject = Subject.objects.get(id=subject_id)
        if not subject.qr_code:
            return Response({"error": "QR code not found for this subject"}, status=status.HTTP_404_NOT_FOUND)

        # Return the QR code URL or file path
        qr_code_url = request.build_absolute_uri(subject.qr_code.url)
        return Response({"qr_code_url": qr_code_url}, status=status.HTTP_200_OK)

    except Subject.DoesNotExist:
        return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)



class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CustodianViewSet(viewsets.ModelViewSet):
    queryset = Custodian.objects.all()
    serializer_class = CustodianSerializer

class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    def create(self, request, *args, **kwargs):
        subject_id = request.data.get('subject_id')
        subject = Subject.objects.get(id=subject_id)
        alarm = Alarm.objects.create(subject=subject)

        # Send WhatsApp message to custodians
        for custodian in subject.custodians.all():
            send_whatsapp_message(custodian.whatsapp_number, f"Alarm triggered for {subject.name}!")

        return Response({"message": "Alarm triggered", "subject_id": subject.id}, status=status.HTTP_201_CREATED)

def send_whatsapp_message(phone_number, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=twilio_whatsapp_number,
            to=f'whatsapp:{phone_number}'
        )
        print(f"WhatsApp message sent: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return False

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_qr_code_api(request):
    subject_id = request.data.get('subject_id')
    subject = Subject.objects.get(id=subject_id)
    qr_code_file = generate_qr_code(subject.id)
    subject.qr_code.save(f'qr_code_{subject.id}.png', qr_code_file)
    subject.save()
    return Response({"message": "QR code generated", "subject_id": subject.id})

def generate_qr_code(subject_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"subject_id:{subject_id}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code_file = File(buffer, name=f'qr_code_{subject_id}.png')
    return qr_code_file