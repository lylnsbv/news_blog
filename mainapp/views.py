from django.shortcuts import render
from django.views.generic import View, ListView
from news.models import Articles, Category
from .forms import ContactForm
from django.db.models import Count
from django.core.mail import send_mail


class BaseView(ListView):
    def get(self, request, *args, **kwargs):
        news = Articles.objects

        context = {
            'news': news.order_by('-post_date'),
            'top_news': news.annotate(total=Count('likes')).order_by('-total'),
            'top_comments': news.annotate(count=Count('comments')).order_by('-count'),
            'today_pick': news.annotate(count_c=Count('comments'), count_l=Count('likes')).order_by('-count_c', '-count_l')[:4],
            'cat_newest': news.distinct('category_id').order_by('category_id', 'post_date')
        }

        return render(request, 'main/home.html', context)


class AboutView(View):
    context = {
        'title': 'О нас'
    }

    def get(self, request):

        return render(request, 'main/about.html', self.context)


class ContactView(View):

    context = {
        'title': 'Контакты',
        'form': ContactForm()
    }

    def get(self, request):
        return render(request, 'main/contact.html', self.context)

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = f"{email} : {form.cleaned_data['message']}"

            form.save()
            send_mail(
                'Сообщение от ' + name,
                message,
                email,
                ['your email'],
                fail_silently=False,
            )
            return render(request, 'main/contact.html', {'sent': name})

        return render(request, 'main/contact.html', self.context)
