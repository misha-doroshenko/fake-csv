from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Schema(models.Model):
    SEPARATOR_CHOICES = (
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        (" ", "Space ( )"),
        ("|", "Pipe (|)"),
    )
    STRING_CHAR_CHOICES = (
        ("'", "Single-quote (')"),
        ("\"", "Double-quote (\")"),
    )
    name = models.CharField(max_length=50)
    column_separator = models.CharField(
        max_length=1,
        choices=SEPARATOR_CHOICES,
        default=",",
    )
    string_character = models.CharField(
        max_length=1,
        choices=STRING_CHAR_CHOICES,
        default="\"",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schemas"
    )
    modified = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Column(models.Model):
    TYPE_CHOICES = (
        ("FN", "Full name"),
        ("Job", "Job"),
        ("Email", "Email"),
        ("PN", "Phone number"),
        ("СN", "Company name"),
        ("Int", "Integer"),
        ("Address", "Address"),
        ("Date", "Date"),

    )
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    min_int = models.IntegerField(null=True, blank=True)
    max_int = models.IntegerField(null=True, blank=True)
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="columns"
    )

    def __str__(self):
        return self.name


class FileCSV(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    created = models.DateField(auto_now_add=True)
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="files"
    )
    rows = models.IntegerField(validators=[MinValueValidator(1)])
