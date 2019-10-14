from api.apps.core.renders import ApiJSONRender


class LicenceJSONRenderer(ApiJSONRender):
    object_label = 'licence'
    pagination_object_label = 'licences'
    pagination_count_label = 'licencesCount'


class CommentJSONRenderer(ApiJSONRender):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'

