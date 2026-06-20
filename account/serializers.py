from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate(self, attr):
        password = attr.get('password')
        password2 = attr.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password does not match")
        return attr
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(name=validated_data.get('name'), email=validated_data.get('email'))

        user.set_password(validated_data.get('password'))
        user.save()

        return user

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer): 
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user:
            raise serializers.ValidationError("Authentication required.")
        print(user.name)
        old_password = attrs.get('old_password')
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        # 2. SECURITY CHECK: Verify the old password matches the database hash
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Your current password is incorrect."})

        if new_password1 != new_password2:
            raise serializers.ValidationError({"new_password2": "New passwords do not match."})

        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password1')
        
        instance.set_password(new_password)
        instance.save()
        
        return instance


