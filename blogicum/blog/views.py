from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . import models
from django.http import Http404
from django.utils import timezone


def index(request):
    post = (
        models.Post.objects.select_related("author", "location", "category")
        .order_by("pub_date")
        .filter(
            Q(pub_date__lte=timezone.now())
            & Q(is_published=True)
            & Q(category__is_published=True)
        )[0:5]
    )
    return render(request, "blog/index.html", {"post_list": post})


def category_posts(request, category_slug):
    category = get_object_or_404(models.Category, slug=category_slug)
    if category.is_published == False:
        raise Http404
    context = {
        "category": category,
        "post_list": models.Post.objects.select_related("location").filter(
            Q(category__slug=category_slug)
            & Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
        ),
    }
    return render(request, "blog/category.html", context)


def post_detail(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post = models.Post.objects.select_related("author", "location", "category").get(pk=pk)
    # models.Post.objects.select_related("author", "location", "category")
    if (
        post.pub_date > timezone.now()
        or post.is_published == False
        or post.category.is_published == False
    ):
        raise Http404
    return render(request, "blog/detail.html", {"post": post})


# class PostDetailView(DetailView):
#     model = models.Post
#     template_name = 'blog/detail.html'

# class IndexTemplateView(TemplateView):
#     model = models.Post
#     template_name = 'blog/index.html'

# class CategoryListView(ListView):
#     model.
