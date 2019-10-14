from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Licence, Comment, Tag
from .renderers import LicenceJSONRenderer, CommentJSONRenderer
from .serializers import LicenceSerializer, CommentSerializer, TagSerializer


class LicenceViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    lookup_field = 'slug'
    queryset = Licence.objects.select_related('sold_by', 'sold_by__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (LicenceJSONRenderer,)
    serializer_class = LicenceSerializer

    def get_queryset(self):
        queryset = self.queryset

        sold_by = self.request.query_params.get('sold_by', None)
        if sold_by is not None:
            queryset = queryset.filter(sold_by__user__username=sold_by)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        sold_by = self.request.query_params.get('sold_by')
        if sold_by is not None:
            queryset = queryset.filter(
                sold_by__user__username=sold_by
            )

        return queryset

    def create(self, request):
        serializer_context = {
            'sold_by': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('licence', {})

        serializer = self.serializer_class(
            data=serializer_data,
            context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Licence.DoesNotExist:
            raise NotFound('An licence with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Licence.DoesNotExist:
            raise NotFound('An licence with this slug does not exist.')

        serializer_data = request.data.get('licence', {})

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class CommentsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'licence__slug'
    lookup_url_kwarg = 'licence_slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        'licence', 'licence__sold_by', 'article__sold_by__user',
        'sold_by', 'sold_by__user'
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}

        return queryset.filter(**filters)

    def create(self, request, *args, licence_slug=None):
        data = request.data.get('comment', {})
        context = {'sold_by': request.user.profile}

        try:
            context['licence'] = Licence.objects.get(slug=licence_slug)
        except Licence.DoesNotExist:
            raise NotFound('An licence with this slug does not exist. ')

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentsDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'comments_pk'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def destroy(self, request, licence_slug=None, comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LicenceSoldAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (LicenceJSONRenderer,)
    serializer_class = LicenceSerializer

    def post(self, request, licence_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            licence = Licence.objects.get(slug=licence_slug)
        except Licence.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.sold(licence)
        licence.sold_by(profile)

        serializer = self.serializer_class(licence, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)


class LicencesListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Licence.objects.all()
    renderer_classes = (LicenceJSONRenderer,)
    serializer_class = LicenceSerializer

    def get_queryset(self):
        return Licence.objects.filter(
            sold_by__in=self.request.user.profile.follows.all()
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)














