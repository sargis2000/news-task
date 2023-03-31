from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.

__all__ = ("Category", "News")


class Category(models.Model):
    """
    A model to represent a news category.

    Attributes:
    -----------
    name : str
        The name of the category.
    slug : str
        A unique slug used to identify the category in URLs.

    Methods:
    --------
    __str__()
        Returns a string representation of the category object.
    get_absolute_url()
        Returns the URL for the category detail page.
    """

    name: str = models.CharField(max_length=64, unique=True, verbose_name="name")
    slug: str = models.SlugField(verbose_name="slug")

    def __str__(self) -> str:
        """
        Returns a string representation of the category object.

        Returns:
        --------
        str:
            The name of the category.
        """
        return self.name

    def get_absolute_url(self) -> str:
        """
        Returns the URL for the category detail page.

        Returns:
        --------
        str:
            The URL for the category detail page.
        """
        return reverse("category_detail", args=[str(self.slug)])

    class Meta:
        """
        Meta options for the Category model.

        Attributes:
        -----------
        verbose_name : str
            A human-readable name for the model.
        verbose_name_plural : str
            The plural form of the verbose name.
        db_table : str
            The name of the database table to use for the model.
        """

        verbose_name: str = "Categories"
        verbose_name_plural: str = "Categories"
        db_table: str = "categories"


class News(models.Model):
    """
    A model class representing a news article.

    Attributes:
    -----------
    title : str
        The title of the news article.
    slug : SlugField
        A unique slug to identify the news article.
    text : RichTextField
        The content of the news article.
    main_category : ForeignKey
        A foreign key relationship to the main category of the news article.
    add_category : ManyToManyField
        A many-to-many relationship to additional categories for the news article.
    created_at : DateTimeField
        The datetime when the news article was created.

    Methods:
    --------
    __str__()
        Returns the title of the news article.
    get_absolute_url()
        Returns the absolute URL of the news article.
    """

    title = models.CharField(max_length=64, unique=True, verbose_name="title")
    slug = models.SlugField(verbose_name="slug")
    text = RichTextField(verbose_name="news content")
    main_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="main category",
        related_name="main_category_news",
    )
    add_category = models.ManyToManyField(
        Category,
        verbose_name="additional category",
        related_name="additional_category_news",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self) -> str:
        """
        Returns the title of the news article.

        Returns:
        --------
        title : str
            The title of the news article.
        """
        return self.title

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL of the news article.

        Returns:
        --------
        url : str
            The absolute URL of the news article.
        """
        return reverse("news_detail", args=[str(self.slug)])

    class Meta:
        """
        Meta options for the Category model.

        Attributes:
        -----------
        verbose_name : str
            A human-readable name for the model.
        verbose_name_plural : str
            The plural form of the verbose name.
        db_table : str
            The name of the database table to use for the model.
        """

        verbose_name = "News"
        verbose_name_plural = "News"
        db_table = "news"


@receiver(post_migrate)
def add_news(sender, **kwargs) -> None:
    """
    Create 20 instances of the News model, each with a unique title, a slug based on the title, some dummy text, a random
    main category, 0-3 random additional categories, and a random creation time

    :param sender: The model class
    """
    from random import randint

    from django.utils import timezone
    from django.utils.text import slugify

    # This is a check to see if the News and Category models have any instances.
    # If they do, then the function will return
    # and not create any more instances.
    if News.objects.exists() or Category.objects.exists():
        return

    for i in range(10):
        Category.objects.create(name=f"Category{i}", slug=slugify(f"Category {i}"))

    # Create 20 instances of the News model
    for i in range(200):
        # Generate a unique title for the news
        title = f"News Title {i}"

        # Generate a slug for the news based on the title
        slug = slugify(title)

        # Generate some dummy text for the news
        text = (
            f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin vel eros ac dui volutpat ultricies. "
            f"Donec fermentum urna ut arcu suscipit vestibulum."
        )

        # Get a random main category for the news
        main_category = Category.objects.order_by("?").first()

        # Get 0-3 random additional categories for the news
        add_categories = Category.objects.order_by("?")[: randint(0, 3)]

        # Generate a random datetime for the news creation time
        created_at = timezone.now() - timezone.timedelta(days=randint(0, 365))

        # Create the news instance and save it to the database
        news = News.objects.create(
            title=title,
            slug=slug,
            text=text,
            main_category=main_category,
            created_at=created_at,
        )
        news.add_category.add(*add_categories)
