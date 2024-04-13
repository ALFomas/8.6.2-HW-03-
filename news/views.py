from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    """ View for post list page """
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    ordering = ['-data_create']
    paginate_by = 5


class SearchList(ListView):
    """ View for search list page """
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-data_create']
    paginate_by = 5

    def get_queryset(self):
        """ method that creates special queries to the database """
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """method that returns the queryset attribute if it is defined"""
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    """ View for post detail page """
    model = Post
    template_name = 'one_post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    """ View for create news post"""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        """ Method for specifying the type"""
        post = form.save(commit=False)
        post.post_type = "NE"
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ View for edit news/articles post"""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'


class NewsDelete(DeleteView):
    """ View for delete news/articles post"""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    """ View for create articles post"""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.add_post'


    def form_valid(self, form):
        """ Method for specifying the type"""
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ View for edit news/articles post"""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'


class ArticlesDelete(DeleteView):
    """ View for edit news/articles post"""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
