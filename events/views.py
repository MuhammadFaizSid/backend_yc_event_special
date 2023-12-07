from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from events.models import Event, UserRecord
from events.serializers import EventSerializer, UserRecordSerializer, GenerateTicketSerializer, SendViaEmailSerializer
from backend_yc_event_special.renderers import CustomRenderer
from rest_framework.pagination import PageNumberPagination
from events.utils import generate_ticket, send_email
from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class EventListCreateView(ListCreateAPIView):
    renderer_classes = [CustomRenderer]
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-id')
    pagination_class = PageNumberPagination


class EventRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    renderer_classes = [CustomRenderer]
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-id')


class UserRecordListCreateView(ListCreateAPIView):
    # renderer_classes = [CustomRenderer]
    serializer_class = UserRecordSerializer
    queryset = UserRecord.objects.all().order_by('-id')
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'encoded_bar_code']


class UserRecordRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    renderer_classes = [CustomRenderer]
    serializer_class = UserRecordSerializer
    queryset = UserRecord.objects.all().order_by('-id')

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class GenerateTicketView(APIView):
    def post(self, request, format=None):
        serializer = GenerateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_id = serializer.data.get("event")
        user_record_id = serializer.data.get("user_record")

        # try: 
        print(event_id)
        event = Event.objects.get(id=event_id)
        user_record = UserRecord.objects.get(id=user_record_id)
        ticket, encoding_code = generate_ticket(event.slug, user_record.sno, event.ticket_featured_photo, user_record.name, user_record.phone_number, user_record.id)

        user_record.encoded_bar_code = encoding_code
        user_record.e_ticket = ticket
        user_record.save()

        return Response({"message": "Ticket Generated Succesfully.", "ticket": ticket}, status=status.HTTP_200_OK)


class SendViaEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendViaEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_record_id = serializer.data.get("user_record")

        # try: 

        user_record = UserRecord.objects.get(id=user_record_id)

        body = f"""Assalam o Alaikum Warehmatullahi Wabarakatuhu {user_record.name.title()}<br/><br/> Your registration for the Youth Club's WOC Mega Event ({user_record.event.event_name.title()}) Hyderabad has been confirmed!<br/><br/> Show this E-Ticket to the registration desk on the event day.<br/><br/>Note: The QR code mentioneded in the E-Ticket is only one time valid, don't share this E-Ticket with anyone. <br/><br/> Venue: {user_record.event.venue} <br/><br/> Pin Location: {user_record.event.location}"""
        print('\n\n', f"https://521d-2400-adc3-111-8400-1036-99ba-f989-5102.ngrok-free.app/media/{user_record.e_ticket}", '\n\n\n')

        send_email(f"Your E-Ticket to '{user_record.event.event_name.title()}' Event by Youth Club!", body, user_record.email, media=True, media_path=f"{user_record.e_ticket}")

        return Response({"message": "Email Sent Succesfully.", "email_sent": True}, status=status.HTTP_200_OK)



        # except Exception as e: 
            # print(e)
            # return Response({"message": "Please provide a valid user id or event id."}, status=status.HTTP_400_BAD_REQUEST)


        # usernames = [user.username for user in User.objects.all()]
        # return Response(usernames)