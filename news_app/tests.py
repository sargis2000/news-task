import datetime
from random import randint

from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, News
from .views import IndexView


class BaseSetup(TestCase):
    """
    Base test class that sets up initial data for the test cases.

    This class creates 10 categories and 20 news articles with random categories assigned to them.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create initial data for the test cases.

        This method creates 10 categories and 20 news articles with random categories assigned to them.
        """
        for i in range(10):
            cat = Category(name=f"Category {i}", slug=f"Category-{i}")
            cat.save()
        for i in range(20):
            main_category = Category.objects.order_by("?").first()
            add_categories = Category.objects.order_by("?")[: randint(0, 3)]
            news = News(
                title=f"news{i}",
                slug=f"news{i}",
                text="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum"
                " has been the industrys standard dummy text ever since the 1500s, when an unknown printer took "
                "a galley of type and scrambled it to make a type specimen book. I",
                main_category=main_category,
            )
            news.save()
            news.add_category.add(*add_categories)


class IndexViewTest(BaseSetup):
    """
    A test suite for testing the IndexView.
    """

    def test_view_url_accessible_by_name(self) -> None:
        """
        Test that the index view can be accessed by its name.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        """
        Test that the index view uses the correct template.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_view_pagination_is_ten(self) -> None:
        """
        Test that the index view paginates the news articles with 10 articles per page.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["all_news"]) == 10)

    def test_view_lists_all_news(self) -> None:
        """
        Test that the index view lists all news articles over multiple pages.
        """
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["all_news"]) == 10)


class CategoryViewTest(BaseSetup):
    """
    A test class for testing the Category view.
    """

    def setUp(self) -> None:
        """
        Sets up the test by creating a Client instance.
        """
        self.client = Client()

    def test_view_url_exists_at_desired_location(self) -> None:
        """
        Tests if the view URL exists at the desired location.
        """
        response = self.client.get("/categories/test-category/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self) -> None:
        """
        Tests if the view URL is accessible by name.
        """
        response = self.client.get(reverse("category_detail", args=["test-category"]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self) -> None:
        """
        Tests if the view uses the correct template.
        """
        response = self.client.get(reverse("category_detail", args=["test-category"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news_list.html")

    def test_view_filters_news_by_date(self) -> None:
        """
        Tests if the view filters news by date.
        """
        # Test case 1: Start and end date are both in the future, so no news should be filtered.
        start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
        response = self.client.get(
            reverse("category_detail", args=["test-category"])
            + f"?start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("filtred_news" in response.context)
        self.assertTrue(len(response.context["filtred_news"]) == 0)

        # Test case 2: Start date is in the past and end date is in the future, so no news should be filtered.
        start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
        end_date = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
        response = self.client.get(
            reverse("category_detail", args=["test-category"])
            + f"?start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("filtred_news" in response.context)
        self.assertTrue(len(response.context["filtred_news"]) == 0)

        # Test case 3: Start and end date are both in the past, so no news should be filtered.
        start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime(
            "%Y-%m-%d"
        )
        end_date = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime(
            "%Y-%m-%d"
        )
        response = self.client.get(
            reverse("category_detail", args=["test-category"])
            + f"?start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("filtred_news" in response.context)
        self.assertTrue(len(response.context["filtred_news"]) == 0)
