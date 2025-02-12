from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Base(models.Model):
    is_published = models.BooleanField(
        "Опубликовано",
        blank=False,
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    d = "Добавлено"
    created_at = models.DateTimeField(d, blank=False, auto_now_add=True)

    class Meta:
        abstract = True


class Category(Base):
    title = models.CharField("Заголовок", max_length=256, blank=False)
    description = models.TextField("Описание", blank=False)
    slug = models.SlugField(
        "Идентификатор",
        blank=False,
        unique=True,
        help_text="Идентификатор страницы для URL;" /
        " разрешены символы латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(Base):
    name = models.CharField("Название места", max_length=256, blank=False)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(Base):
    title = models.CharField("Заголовок", max_length=256, blank=False)
    text = models.TextField("Текст", blank=False)
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        blank=False,
        help_text="Если установить дату и время в будущем" /
        " — можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Местоположение",
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        verbose_name="Категория",
        null=True,
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
