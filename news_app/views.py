import datetime

from django.db.models import Model, Q, QuerySet
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .models import *


__all__ = ("IndexView", "CategoryView", "NewsDetailView")


class BaseNewsView(ListView):
    """
    A base view to display a list of news objects with pagination and filtering by date range.
    Attributes:
    -----------
    paginate_by : int
        The number of news objects to display per page.

    Methods:
    --------
    get_queryset()
        Returns the queryset of News objects filtered by date range.
    filter_by_date(queryset)
        Filters the queryset of News objects by date range.
    """

    paginate_by: int = 10

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset of News objects filtered by date range.

        Returns:
        --------
        queryset : QuerySet
            A queryset of News objects filtered by date range.
        """
        queryset = super().get_queryset()
        queryset = self.filter_by_date(queryset)
        return queryset

    def filter_by_date(self, queryset: QuerySet) -> QuerySet:
        """
        Filters the queryset of News objects by date range.

        Parameters:
        -----------
        queryset : QuerySet
            A queryset of News objects.

        Returns:
        --------
        queryset : QuerySet
            A queryset of News objects filtered by date range.
        """
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date and end_date:
            start_datetime = timezone.make_aware(
                datetime.datetime.strptime(start_date, "%Y-%m-%d")
            )
            end_datetime = timezone.make_aware(
                datetime.datetime.strptime(end_date, "%Y-%m-%d")
            )
            queryset = queryset.filter(created_at__range=(start_datetime, end_datetime))
        return queryset


class IndexView(BaseNewsView):
    """
    A view to display the home page which lists all news objects.

    Attributes:
    -----------
    template_name : str
        The name of the template used to render the view.
    context_object_name : str
        The name of the variable to be used as the context object in the template.
    model : Model
        The model used to fetch the news objects.
    ordering : str
        The order in which the news objects should be displayed.

    Methods:
    --------
    None
    """

    template_name: str = "home.html"
    context_object_name: str = "all_news"
    model: Model = News
    ordering: str = "-created_at"


class CategoryView(BaseNewsView):
    """
    A view to display a list of news filtered by a specific category and date range.

    Attributes:
    -----------
    context_object_name : str
        The name of the variable to be used as the context object in the template.
    template_name : str
        The name of the template used to render the view.

    Methods:
    --------
    get_queryset()
        Returns the queryset of News objects filtered by a specific category and date range.
    """

    context_object_name: str = "filtred_news"
    template_name: str = "news_list.html"

    def get_queryset(self) -> QuerySet:
        """
        Returns the queryset of News objects filtered by a specific category and date range.

        Returns:
        --------
        queryset : QuerySet
            A queryset of News objects filtered by a specific category and date range.
        """
        queryset = (
            News.objects.filter(
                Q(main_category__slug=self.kwargs["slug"])
                | Q(add_category__slug=self.kwargs["slug"])
            )
            .order_by("-created_at")
            .distinct()
        )
        queryset = self.filter_by_date(queryset)
        return queryset


class NewsDetailView(DetailView):
    """
    A view to display the details of a specific news object.

    Attributes:
    -----------
    template_name : str
        The name of the template used to render the view.
    context_object_name : str
        The name of the variable to be used as the context object in the template.
    model : Model
        The model used to fetch the news object.

    Methods:
    --------
    None
    """

    template_name: str = "news_detail.html"
    context_object_name: str = "news"
    model: Model = News
