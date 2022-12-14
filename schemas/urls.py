from django.urls import path

from schemas.views import SchemaListView, SchemaCreateView, SchemaUpdateView, schema_files, generate_file

app_name = "schemas"

urlpatterns = [
    path("", SchemaListView.as_view(), name="schema-list"),
    path("schemas/create", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/update/<int:pk>/", SchemaUpdateView.as_view(), name="schema-update"),
    path("schemas/file_csv/<int:pk>/", schema_files, name="schema-files"),
    path("schemas/create_file/<int:pk>/", generate_file, name="create-file"),
]