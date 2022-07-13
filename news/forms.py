from .models import Articles, Category, Comment
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, Select

choices = Category.objects.all().values_list('name', 'name')


class ArticlesForm(ModelForm):

    class Meta:
        model = Articles
        fields = ['title', 'anons', 'author', 'category', 'full_text', 'header_image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'anons': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тег статьи'
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'value': '',
                'id': 'elder',
                'type': 'hidden'
            }),
            'category': Select(choices=choices,
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Категория'
                               }),
            'full_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Тектс статьи'
            })
        }


class EditForm(ModelForm):

    class Meta:
        model = Articles
        fields = ['title', 'anons', 'full_text', 'category', 'post_date', 'header_image']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'anons': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тег статьи'
            }),
            'category': Select(choices=choices,
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Категория'
                               }),
            'post_date': DateTimeInput(attrs={
                'class': 'form-control'
            }),
            'full_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Тектс статьи'
            })
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

        widgets = {

            'body': Textarea(attrs={
                'name': 'message', 'id': 'message'
            })
        }
