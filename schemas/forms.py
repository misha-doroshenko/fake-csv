from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import inlineformset_factory, BaseFormSet, BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from schemas.models import Column, Schema, FileCSV


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Username",
                "class": "form-control font-weight-light",
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
                "class": "form-control font-weight-light",
            }
        ),
    )


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "column_separator", "string_character"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-6"
        self.helper.layout = Layout(
            HTML("<h2>{{ object|yesno:'Edit,New' }} Schema</h2>"),
            ButtonHolder(Submit("submit", "Submit"), css_class="float-right"),
            Div(
                Field("name"),
                Field("column_separator"),
                Field("string_character"),
                Fieldset("Add columns", Formset("column_formset")),
                HTML("<br>"),
            ),
        )


class ColumnForm(forms.ModelForm):
    min_int = forms.IntegerField(required=False, label="From")
    max_int = forms.IntegerField(required=False, label="To")

    class Meta:
        model = Column
        fields = ["name", "type", "min_int", "max_int"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = "pl-2"
        self.helper.field_class = "pl-2"


class RequiredFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


ColumnFormset = inlineformset_factory(
    Schema,
    Column,
    formset=RequiredFormSet,
    form=ColumnForm,
    fields=["name", "type", "min_int", "max_int"],
    extra=1,
    can_delete=True,
)


class FileCSVForm(forms.ModelForm):

    class Meta:
        model = FileCSV
        fields = ["rows"]
        widgets = {
            'rows': forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Rows",
                }
            ),
        }