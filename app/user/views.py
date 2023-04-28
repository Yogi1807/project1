from django.shortcuts import render

from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication, permissions

# Create your views here.


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    TODO
    References
    1. https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

    """

    serializer_class = AuthTokenSerializer


class ManageUserView(RetrieveUpdateAPIView):
    """
    get
    patch
    put

    TODO
    TOPIC - generic views in DRF for get/put/patch (RetrieveUpdateAPIView)
    refer -
    https://www.django-rest-framework.org/api-guide/generic-views/#retrieveupdateapiview
    """

    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]

    # TODO - refer
    # https://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieve user and return authenticated user information

        TODO - refer
        https://www.django-rest-framework.org/api-guide/permissions/#object-level-permissions
        """

        return self.request.user