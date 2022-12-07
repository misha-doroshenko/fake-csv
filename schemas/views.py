from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import generic

from schemas.forms import LoginForm
from schemas.models import Schema


class SchemaListView(LoginRequiredMixin, generic.ListView):
    model = Schema

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user").filter(user__id=self.request.user.id)


class NewLoginView(LoginView):
    form_class = LoginForm


def logout_view(request):
    logout(request)
    return redirect("/")