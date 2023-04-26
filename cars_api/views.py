from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from cars_api.models import Car
from cars_api.forms import PostForm


class PostListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars_api/post/list.html'
    queryset = Car.published.all()
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        period = self.request.GET.get('period')
        owner = self.request.GET.get('owner')
        brand = self.request.GET.get('brand')
        model = self.request.GET.get('model')
        country = self.request.GET.get('country')
        fuel = self.request.GET.get('fuel')
        engine = self.request.GET.get('engine')
        on_sale = self.request.GET.get('on_sale')

        if period == 'day':
            today = timezone.localtime().date()
            queryset = queryset.filter(publish__date=today)
        elif period == 'week':
            start_date = timezone.localtime().date() - timedelta(days=7)
            queryset = queryset.filter(publish__gte=start_date)
        elif period == 'month':
            start_date = timezone.localtime().date() - timedelta(days=30)
            queryset = queryset.filter(publish__gte=start_date)

        if owner:
            owner = get_object_or_404(User, username=owner)
            queryset = queryset.filter(owner=owner)

        if brand:
            queryset = queryset.filter(brand=brand)

        if model:
            queryset = queryset.filter(model=model)

        if country:
            queryset = queryset.filter(country=country)

        if fuel:
            queryset = queryset.filter(fuel=fuel)

        if engine:
            queryset = queryset.filter(engine=engine)

        if on_sale:
            queryset = queryset.filter(on_sale=on_sale)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        query_params = self.request.GET.copy()
        url_without_params = self.request.path

        if page_obj.has_previous():
            query_params['page'] = page_obj.previous_page_number()
            prev_page_url = f'{url_without_params}?{query_params.urlencode()}'
            context['prev_page_url'] = prev_page_url
        if page_obj.has_next():
            query_params['page'] = page_obj.next_page_number()
            next_page_url = f'{url_without_params}?{query_params.urlencode()}'
            context['next_page_url'] = next_page_url

        context['posts'] = page_obj
        return context


class PostDetailView(DetailView):
    model = Car
    template_name = 'cars_api/post/detail.html'
    queryset = Car.published.all()

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        slug = self.kwargs.get('slug')

        queryset = queryset or self.queryset
        post = get_object_or_404(queryset,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 slug=slug)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = PostForm
    template_name = 'cars_api/post/new.html'
    success_url = reverse_lazy('cars_api:post_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.slug = slugify(f'{form.instance.brand}-{form.instance.model}-{form.instance.year}')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = PostForm
    template_name = 'cars_api/post/edit.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Car, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

    def form_valid(self, form):
        form.instance.owner = self.object.owner
        form.instance.slug = slugify(f'{form.instance.brand}-{form.instance.model}-{form.instance.year}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cars_api:post_detail', args=[self.object.publish.year,
                                                     self.object.publish.month,
                                                     self.object.publish.day,
                                                     self.object.slug])


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('cars_api:post_list')

    def form_valid(self, form):
        if self.request.user.is_superuser or self.object.owner == self.request.user:
            messages.success(self.request, f'Post deleted {self.object.brand} {self.object.model}')
            return super().form_valid(form)
        else:
            raise PermissionDenied("You don't have permission to delete this post")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context
