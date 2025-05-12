from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import re

class RegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    class Meta:
        model=User
        fields=['username','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True},
            'email':{'required':True}
        }
        
    def validate_email(self,value):
        email=value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('User with this email already exists..')
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, value):
            raise ValidationError('Enter a valid email address.')

        return email
    
    def validate_username(self,value):
        pattern = r'^[a-zA-Z0-9_-]{3,30}$'
        if not re.match(pattern, value):
            raise ValidationError(
            'Username must be 3-30 characters long and contain only letters, numbers, underscores, or hyphens.'
        )
        return value
    
    def validate(self,data):
        password=data.get('password')
        conf_password=data.get('password2')

        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if not re.match(pattern, password):
            raise serializers.ValidationError("Password must be at least 8 characters and include uppercase," \
                                              " lowercase, number, and special character.")

        if password != conf_password:
            raise serializers.ValidationError({"password": "Password and Confirm Password do not match."})
        
        return data
    
    def create(self, validated_data):
        user=User(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user
    


    


# from django.core.validators import validate_email
# from django.contrib.auth.password_validation import validate_password
# if len(password) < 8:
        #     raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # if not re.search(r'[A-Z]', password):
        #     raise serializers.ValidationError("Password must include at least one uppercase letter.")

        # if not re.search(r'[a-z]', password):
        #     raise serializers.ValidationError("Password must include at least one lowercase letter.")

        # if not re.search(r'\d', password):
        #     raise serializers.ValidationError("Password must include at least one number.")

        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        #     raise serializers.ValidationError("Password must include at least one special character.")
        

    
    