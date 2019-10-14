from django.conf.urls import url
from rest_framework import routers
from .views import ProfileRetrieveAPIView, ProfileFollowAPIView

router = routers.DefaultRouter()
router.register(r'users', vie)

urlpatterns = [
    url(r'^profiles/(?P<username>\w+)/?$', ProfileRetrieveAPIView.as_view()),
    url(r'^profiles/(?P<username>\w+)/?$/follow/?$', ProfileFollowAPIView.as_view()),
]