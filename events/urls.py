from django.urls import path
from events.views import EventListCreateView, EventRetrieveUpdateDestroyView, UserRecordListCreateView, UserRecordRetrieveUpdateDestroyView, GenerateTicketView, SendViaEmailView


urlpatterns = [
    path('event-list-create/', EventListCreateView.as_view(), name='user-record-list-create-event'),
    path('event-retrieve-update-destroy/<int:pk>', EventRetrieveUpdateDestroyView.as_view(), name='event-retrieve-update-destroy'),
    path('user-record-list-create/', UserRecordListCreateView.as_view(), name='list-create-user-record'),
    path('user-record-retrieve-update-destroy/<int:pk>', UserRecordRetrieveUpdateDestroyView.as_view(), name='user-record-retrieve-update-destroy'),
    path('generate-ticket/', GenerateTicketView.as_view(), name='generate-ticket'),
    path('send-email/', SendViaEmailView.as_view(), name='send-via-email'),

]
