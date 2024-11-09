from rest_framework import pagination


class AdPagination(pagination.PageNumberPagination):
    """Пагинация объявлений 4 объекта на странице."""

    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 4
