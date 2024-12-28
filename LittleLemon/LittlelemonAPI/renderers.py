from rest_framework_json_api.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = super().render(data, accepted_media_type, renderer_context)
        return response