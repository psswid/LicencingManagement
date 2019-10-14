from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from .views import (
    LicenceViewSet, LicenceSoldAPIView, LicencesListApiView,
    CommentsListCreateAPIView, CommentsDestroyAPIView, TagListAPIView
)

router = DefaultRouter(trailing_slash=False)
router.register(r'licences', LicenceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^licences/list/?$', LicencesListApiView.as_view()),
    url(r'^licences/(?P<licence_slug>[-\w]+)/sold/?$',
        LicenceSoldAPIView.as_view()),
    url(r'^licences/(?P<licence_slug>[-\w]+)/comments/?$',
        CommentsListCreateAPIView.as_view()),
    url(r'^licences/(?P<licence_slug>[-\w]+)/comments/(?P<comment_pk>[\d]+)/?$',
        CommentsDestroyAPIView.as_view()),
    url(r'^tags/?$', TagListAPIView.as_view()),
]