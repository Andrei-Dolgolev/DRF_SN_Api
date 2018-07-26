from django.contrib.auth.signals import user_logged_in
from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .custom_jwt import jwt_payload_handler
from .serializers import UserSerializer
from .models import User
from .permissions import AnonCreateAndUpdateOwnerOnly
from pyhunter import PyHunter
import jwt
import clearbit


class UserAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AnonCreateAndUpdateOwnerOnly,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = self.api_call()
        if not isinstance(response,dict):
            return response
        data = request.data
        data.update(response)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    Verify email(emailhunter.co) and try get city(clearbit.com)
    :return None in bad case return responce object
    """
    def api_call(self):

        #  request Api emailhunter.co
        hunter_key = '0951ac6a0348e8db1a20fe321c1995aa0bc48bfa'
        try:
            email_status = PyHunter(hunter_key).email_verifier(self.request.data['email'])['result']
            print('email_status',email_status)
        except:
            return Response('Not valid mailbox', status=status.HTTP_406_NOT_ACCEPTABLE)
        if email_status == 'undeliverable':
            return Response('Email undeliverable please provide exists mailbox', status=status.HTTP_406_NOT_ACCEPTABLE)

        # request Api clearbit.com
        clearbit.key = 'sk_00c36392dc89fb53f371529b79e7b4f4'
        try:
            response = clearbit.Enrichment.find(email=self.request.data['email'], stream=True)
        except:
            response = None

        #  get location only
        city_data = {}
        if not response:
            city_data['city'] = 'not response'
        elif response.get('person') is not None:
            city_data['city'] = response['person']['location']
        return city_data

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['email'] = "%s" % (
                    user.email)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)
