from django.forms import CharField
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User=get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(min_length=6, required=True)
    password_confirm= serializers.CharField(min_length=6, required=True)
    name=serializers.CharField(required=True)


    def validate_email(self,email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    
    def validate (self,attrs:dict):
        pass1=attrs.get('password')
        pass2=attrs.pop('password_confirm')
        if pass1!=pass2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    
    def save(self):
        data=self.validated_data
        user=User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_email()



class LoginSerializer(TokenObtainPairSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(min_length=6, required=True)

    def validate_email(self,email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email
    
    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.pop('password')
        user=User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        if user and user.is_active:
            refresh=self.get_token(user)
            attrs['refresh']=str(refresh)
            attrs['access']=str(refresh.access_token)
            #refresh - обновленный токен (нужен frontу)
            #access  - токен для всех
            return attrs

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('email doesnt exist')
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    old_password=serializers.CharField(min_length=6, required=True)
    new_password=serializers.CharField(min_length=6, required=True)
    password_confirm= serializers.CharField(min_length=6, required=True)


    def validate(self,attrs):
        email = attrs.get('email')
        pass1 = attrs.get('old_password')
        pass2=attrs.get('new_password')
        pass3=attrs.pop('password_confirm')

        if email and pass1:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=pass1)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg='User is not active. Please follow the link sent to your mail to activate your account'
                raise serializers.ValidationError(msg,code='authorization')
        
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')


        if pass2!=pass3:
            raise serializers.ValidationError('Passwords do not match')

        attrs['user'] = user
        return attrs



