from django.urls import path

from schemas.views import SchemaListView, SchemaCreateView, SchemaUpdateView

app_name = "schemas"

urlpatterns = [
    path("", SchemaListView.as_view(), name="schema-list"),
    path("schemas/create", SchemaCreateView.as_view(), name="schema-create"),
    path("schemas/update/<int:pk>/", SchemaUpdateView.as_view(), name="schema-update")
]