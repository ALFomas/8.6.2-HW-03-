from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author


class IndexView(LoginRequiredMixin, TemplateView):
    """View profile user!"""
    template_name = 'profile_window.html'

    def get_context_data(self, **kwargs):
        """the method of determining author"""
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    """method for adding authors to the group"""
    user = request.user
    autors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        autors_group.user_set.add(user)
        if not Author.objects.filter(user=user).exists():
            Author.objects.create(user=user)
    return redirect('/')
