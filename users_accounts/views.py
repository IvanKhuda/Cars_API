from django.contrib.auth.views import LogoutView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from users_accounts.forms import LoginForm, RegisterForm


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('cars_api:post_list')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('accounts:login'))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)
