from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for the Category model.

    Attributes:
    -----------
    list_display : tuple
        A tuple containing the names of fields to display in the changelist view.
    prepopulated_fields : dict
        A dictionary of field names and the corresponding fields from which to populate them.
    search_fields : tuple
        A tuple containing the names of fields to search for in the admin interface.
    """

    list_display: tuple = ("name",)
    prepopulated_fields: dict = {"slug": ("name",)}
    search_fields: tuple = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """
    Admin class for the News model.

    Attributes:
    -----------
    list_display : tuple
        A tuple containing the names of fields to display in the changelist view.
    prepopulated_fields : dict
        A dictionary of field names and the corresponding fields from which to populate them.
    ordering : tuple
        A tuple containing the names of fields to use when ordering the results in the changelist view.
    search_fields : tuple
        A tuple containing the names of fields to search for in the admin interface.
    list_filter : tuple
        A tuple containing the names of fields to use as filters in the changelist view.
    """

    list_display: tuple = ("title", "main_category", "created_at")
    prepopulated_fields: dict = {"slug": ("title",)}
    ordering: tuple = ("created_at",)
    search_fields: tuple = ("title",)
    list_filter: tuple = (
        "main_category",
        "add_category",
        "created_at",
    )
