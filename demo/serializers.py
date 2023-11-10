import random
from rest_framework import serializers
import random
from datetime import datetime, timedelta
from .models import UserModel
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True, min_length = settings.MIN_PASSWORD_LENGTH, 
        error_messages = {"min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters"}
    )
    password2 = serializers.CharField(
        write_only=True, min_length = settings.MIN_PASSWORD_LENGTH, 
        error_messages = {"min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters"}
    )
    otp = serializers.CharField(read_only=True, min_length=4)
    
    
    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "password1",
            "password2",
            "otp"
        )
        
    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Password do not match. ")
        return data

    def create(self, validated_data):
        otp = random.randint(1000,9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        user = UserModel(
            phone_number = validated_data["phone_number"],
            email = validated_data["email"],
            otp = otp,
            otp_expiry = otp_expiry,
            max_otp_try = settings.MAX_OTP_TRY
        )
        
        user.set_password(validated_data["password1"])
        user.save()
        # TODO: call send_otp function
        return user