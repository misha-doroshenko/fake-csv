import datetime
from io import BytesIO

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from schemas.forms import LoginForm, SchemaForm, ColumnFormset, FileCSVForm
from schemas.models import Schema, Column, FileCSV


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


def schema_files(request, pk):
    schema = Schema.objects.get(id=pk)
    columns = list(Column.objects.filter(schema_id=pk))
    files = list(FileCSV.objects.filter(schema_id=pk))
    form = FileCSVForm

    if request.method == "POST":
        response, context = {}, {}
        form = FileCSVForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.file = "/Users/doroshenko/projects/fake_csv/test.csv"
            form.instance.schema = schema
            record = form.save()
            file_name = "test.txt"
            file_content = b"I have my full 100% power now!"
            file_content_io = BytesIO(file_content)

            default_storage.save(file_name, file_content_io)
            # rendered = render_to_string('schemas/file_csv.html',
            #                             {'record': record})  # якщо треба відображати якісь результати (напр. коментарі)
            context = {'id': record.id, 'rows': record.rows, 'result': 'success'}
        else:
            k = 0
            for error in form.errors:
                response[k] = form.errors[error][0]
                context = {'response': response, 'result': 'error'}
                k += 1
        return JsonResponse(context)

    return render(
        request,
        "schemas/file_csv.html",
        {"form": form, "schema": schema, "columns": columns, "files": files}
    )


def generate_file(request, pk):
    schema = Schema.objects.get(id=pk)
    if request.method == "POST":
        response, context = {}, {}
        form = FileCSVForm(request.POST)
        if form.is_valid():
            form.instance.file = "/Users/doroshenko/projects/fake_csv/test.csv"
            form.instance.schema = schema
            record = form.save()
            # rendered = render_to_string('schemas/file_csv.html',
            #                             {'record': record})  # якщо треба відображати якісь результати (напр. коментарі)
            context = {'id': record.id, 'rows': record.rows, 'result': 'success'}
        else:
            k = 0
            for error in form.errors:
                response[k] = form.errors[error][0]
                context = {'response': response, 'result': 'error'}
                k += 1
        return JsonResponse(context)

# def create_post(request):
#     if request.method == 'POST':
#         post_text = request.POST.get('the_post')
#         response_data = {}
#
#         post = Post(text=post_text, author=request.user)
#         post.save()
#
#         response_data['result'] = 'Create post successful!'
#         response_data['postpk'] = post.pk
#         response_data['text'] = post.text
#         response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
#         response_data['author'] = post.author.username
#
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )