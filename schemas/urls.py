from django.urls import path

from schemas.views import SchemaListView, SchemaCreateView, SchemaUpdateView, schema_files, SchemaDeleteView

app_name = "schemas"

urlpatterns = [
    path("", SchemaListView.as_view(), name="schema-list"),
    path("schemas/create", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/update/<int:pk>/", SchemaUpdateView.as_view(), name="schema-update"),
    path("schemas/delete/<int:pk>/", SchemaDeleteView.as_view(), name="schema-delete"),
    path("schemas/file_csv/<int:pk>/", schema_files, name="schema-files"),
]