from api.apps.core.renders import ApiJSONRender


class ProfileJSONRenderer(ApiJSONRender):
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'