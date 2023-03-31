# Generated by Django 4.1.7 on 2023-03-31 10:25

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="name"),
                ),
                ("slug", models.SlugField(verbose_name="slug")),
            ],
            options={
                "verbose_name": "Categories",
                "verbose_name_plural": "Categories",
                "db_table": "categories",
            },
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=64, unique=True, verbose_name="title"),
                ),
                ("slug", models.SlugField(verbose_name="slug")),
                ("text", ckeditor.fields.RichTextField(verbose_name="news content")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "add_category",
                    models.ManyToManyField(
                        blank=True,
                        related_name="additional_category_news",
                        to="news_app.category",
                        verbose_name="additional category",
                    ),
                ),
                (
                    "main_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_category_news",
                        to="news_app.category",
                        verbose_name="main category",
                    ),
                ),
            ],
            options={
                "verbose_name": "News",
                "verbose_name_plural": "News",
                "db_table": "news",
            },
        ),
    ]