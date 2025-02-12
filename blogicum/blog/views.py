from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . import models as m
from django.http import Http404
from django.utils import timezone


def index(request):
    post = (
        m.Post.objects.select_related("author", "location", "category")
        .order_by("pub_date")
        .filter(
            Q(pub_date__lte=timezone.now())
            & Q(is_published=True)
            & Q(category__is_published=True)
        )[0:5]
    )
    c = {"post_list": post}
    t = "blog/index.html"
    return render(request, t, c)


def category_posts(request, category_slug):
    category = get_object_or_404(m.Category, slug=category_slug)
    if category.is_published is False:
        raise Http404
    context = {
        "category": category,
        "post_list": m.Post.objects.select_related("location").filter(
            Q(category__slug=category_slug)
            & Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
        ),
    }
    t = "blog/category.html"
    return render(request, t, context)


def post_detail(request, pk):
    post = get_object_or_404(m.Post, pk=pk)
    a = "author"
    lo = "location"
    c = "category"
    post = m.Post.objects.select_related(a, lo, c).get(pk=pk)
    if (
        post.pub_date > timezone.now()
        or post.is_published is False
        or post.category.is_published is False
    ):
        raise Http404
    con = {"post": post}
    t = "blog/detail.html"
    return render(request, t, con)


# class PostDetailView(DetailView):
#     model = models.Post
#     template_name = 'blog/detail.html'

# class IndexTemplateView(TemplateView):
#     model = models.Post
#     template_name = 'blog/index.html'

# class CategoryListView(ListView):
#     model.
