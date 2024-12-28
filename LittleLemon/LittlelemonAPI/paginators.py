from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework.response import Response

class CustomPagination(JsonApiPageNumberPagination):
    def get_first_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return self.replace_query_param(url, self.page_query_param, 1)

    def get_last_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return self.replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'links': {
                'first': self.get_first_link(),
                'last': self.get_last_link(),
                'next': self.get_next_link(),
                'prev': self.get_previous_link()
            },
            'meta': {
                'pagination': {
                    'current_page': self.page.number,
                    'from': self.page.start_index(),
                    'last_page': self.page.paginator.num_pages,
                    'path': self.request.build_absolute_uri(),
                    'per_page': self.page.paginator.per_page,
                    'to': self.page.end_index(),
                    'total': self.page.paginator.count,
                }
            }
        })
