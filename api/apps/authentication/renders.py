from api.apps.core.renders import ApiJSONRender


class UserJSONRenderer(ApiJSONRender):
    charset = 'utf-8'
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_object_count = 'usersCount'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)