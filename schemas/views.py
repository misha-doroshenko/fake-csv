import datetime

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from schemas.forms import LoginForm, SchemaForm, ColumnFormset
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


class SchemaCreateView(generic.edit.CreateView):
    model = Schema
    template_name = "../templates/schemas/schema_form.html"
    form_class = SchemaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ColumnFormset.extra = 1
        if self.request.POST:
            data['column_formset'] = ColumnFormset(self.request.POST)
        else:
            data['column_formset'] = ColumnFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['column_formset']
        form.instance.user = self.request.user
        if columns.is_valid() and form.is_valid():
            self.object = form.save()
            columns.instance = self.object
            columns.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:schema-list')


class SchemaUpdateView(generic.edit.UpdateView):
    model = Schema
    template_name = "../templates/schemas/schema_form.html"
    form_class = SchemaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ColumnFormset.extra = 0
        if self.request.POST:
            data['column_formset'] = ColumnFormset(self.request.POST, instance=self.object)
        else:
            data['column_formset'] = ColumnFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['column_formset']
        if columns.is_valid() and form.is_valid():
            self.object = form.save()
            form.instance.modified = datetime.date.today()
            columns.instance = self.object
            columns.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:schema-list')
