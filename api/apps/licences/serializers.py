from rest_framework import serializers

from api.apps.profiles.serializers import ProfileSerializer

from .models import Licence, Comment, Tag
from .relations import TagRelatedField


class LicenceSerializer(serializers.HyperlinkedModelSerializer):
    sold_by = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    sold = serializers.SerializerMethodField()
    soldCount = serializers.SerializerMethodField(
        method_name='get_sold_count'
    )

    tagList = TagRelatedField(many=True, required=False, source='tags')

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Licence
        fields = (
            'sold_by',
            'body',
            'createdAt',
            'description',
            'sold',
            'soldCount',
            'slug',
            'tagList',
            'title',
            'updatedAt'
        )

    def create(self, validated_data):
        sold_by = self.context.get('sold_by', None)

        tags = validated_data.pop('tags', [])

        licence = Licence.objects.create(sold_by=sold_by, **validated_data)

        for tag in tags:
            licence.tags.add(tag)

        return licence

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_sold(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated():
            return False

        return request.user.profile.has_solded(instance)

    def get_sold_count(self, instance):
        return instance.sold_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    sold_by = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'sold_by',
            'body',
            'createdAt',
            'updatedAt'
        )

    def create(self, validated_data):
        license = self.context['licence']
        sold_by = self.context['sold_by']

        return Comment.objects.create(
            sold_by=sold_by, license=license, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

        def to_representation(self, obj):
            return obj.tag