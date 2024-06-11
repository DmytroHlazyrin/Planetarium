# custom_schema_generator.py

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.openapi import AutoSchema
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CustomSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        # Получение базовой схемы
        schema = super().get_schema(request, public)

        if request is not None and not request.user.is_staff:
            paths_to_remove = []

            for path, methods in schema['paths'].items():
                methods_to_remove = []

                for method, details in methods.items():
                    # Получаем представление (view) для каждого метода
                    view = self.view_from_method(method, path)

                    # Проверяем права доступа для представления
                    if not self.check_permissions(request, view):
                        methods_to_remove.append(method)

                for method in methods_to_remove:
                    del methods[method]

                # Если все методы для пути удалены, удаляем путь
                if not methods:
                    paths_to_remove.append(path)

            for path in paths_to_remove:
                del schema['paths'][path]

        return schema

    def view_from_method(self, method, path):
        # Получаем представление (view) для метода и пути
        for view in self.view_endpoints:
            if view[0] == path and view[1] == method:
                return view[4].cls()
        return None

    def check_permissions(self, request, view):
        # Проверяем права доступа для представления
        for permission in view.permission_classes:
            if not permission().has_permission(request, view):
                return False
        return True
