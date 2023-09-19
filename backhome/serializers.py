from rest_framework import serializers
from .models import URLModel

class URLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLModel
        fields = '__all__'
