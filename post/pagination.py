from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 50


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5