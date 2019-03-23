from rest_framework import serializers

class GiftRecipientSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    street_address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=2)
    zip_code = serializers.CharField(max_length=5)
