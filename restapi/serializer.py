from rest_framework import serializers
from .models import friend_suggestor


class serializer_register(serializers.ModelSerializer):
    class Meta:
        model = friend_suggestor
        fields = ('id',
                  'username')
