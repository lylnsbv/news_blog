from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from .models import Articles, Category
from .forms import ArticlesForm, EditForm, CommentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Count


class CategoryView(DetailView):

    model = Category
    context_object_name = 'category'
    template_name = 'newshtml/categories.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = Articles.objects
        category_posts = news.filter(category_id=self.object.id)
        context["category_posts"] = category_posts
        context['top_news'] = news.annotate(total=Count('likes')).order_by('-total')
        context['today_pick'] = news.annotate(count_c=Count('comments'),
                                              count_l=Count('likes')).order_by('-count_c', '-count_l')[:4]
        return context


class NewsDetailView(DetailView):

    model = Articles
    template_name = 'newshtml/details_view.html'
    context_object_name = 'article'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('news-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        news = self.model.objects
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Articles, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context['comment_form'] = CommentForm(initial={
            'article': self.object
        })

        context['top_news'] = news.annotate(total=Count('likes')).order_by('-total')
        context['today_pick'] = news.annotate(count_c=Count('comments'),
                                              count_l=Count('likes')).order_by('-count_c', '-count_l')[:4]
        return context

    def post(self, request):
        post = get_object_or_404(Articles, pk=self.kwargs['pk'])
        if request.method == 'POST':
            form = CommentForm(request.POST, request.FILES)

            if form.is_valid():
                form.instance.name = request.user
                comment = form.save(commit=False)
                comment.post = post

                comment.save()
                return redirect('news-detail', pk=post.pk)
            else:
                form = CommentForm()

        return reverse_lazy('news-detail', pk=self.kwargs['pk'])


class NewsUpdateView(UpdateView):

    model = Articles
    template_name = 'newshtml/update_post.html'
    form_class = EditForm

    def get_context_data(self, *args, **kwargs):
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        return context


class NewsDeleteView(DeleteView):

    model = Articles
    success_url = reverse_lazy('home')
    template_name = 'newshtml/news-delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super(NewsDeleteView, self).get_context_data(**kwargs)
        return context


class AddPostView(CreateView):

    def get(self, request, *args, **kwargs):

        form = ArticlesForm()
        context = {
            'form': form,
        }
        return render(request, 'newshtml/add_post.html', context)

    def post(self, request, *args, **kwargs):
        error = ''
        if request.user.is_authenticated:
            if request.method == 'POST':
                form = ArticlesForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('home')
                else:
                    error = 'Форма была неверной'

        context = {
            'error': error
        }
        return render(request, 'newshtml/add_post.html', context)

    def get_context_data(self, *args, **kwargs):
        context = super(AddPostView, self).get_context_data(**kwargs)
        return context


class AddCategoryView(CreateView):

    model = Category
    template_name = 'newshtml/add_category.html'
    fields = ['name']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        context["cat_menu"] = cat_menu
        return context


def LikeView(request, pk):
    article = get_object_or_404(Articles, id=request.POST.get('article_id'))
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('news-detail', args=[str(pk)]))
