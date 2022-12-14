from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from schemas.models import User, Column, Schema, FileCSV


@admin.register(User)
class DriverAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )


admin.site.register(Column)
admin.site.register(Schema)
admin.site.register(FileCSV)
