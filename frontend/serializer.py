from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializers(serializers.Serializers):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(username = email, password = password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password")
            else:
                raise serializers.ValidationError("Email and password are required.")
            data["user"] = user
            return data
            