from rest_framework import serializers
from events.models import Event, UserRecord

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
class UserRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecord
        fields = '__all__'

class GenerateTicketSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    user_record = serializers.IntegerField()


class SendViaEmailSerializer(serializers.Serializer):
    user_record = serializers.IntegerField()

