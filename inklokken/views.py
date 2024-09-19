from datetime import datetime

import django.contrib.auth.views
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import ClockInForm, SickLeaveForm
from .models import CompanyNews, Event


class LoginView(django.contrib.auth.views.LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = CompanyNews.objects.all()
        context["company_news"] = news

        if self.request.user.is_staff:
            User = get_user_model()
            # users = User.objects.filter(~Q(username=self.request.user.username)).all()
            users = User.objects.all()
            users_clocked_in = Event.objects.filter(
                event_type="clock_in", event_from__gte=datetime.now().date()
            ).all()
            clocked_in_users = {}
            for user_clock_in in users_clocked_in:
                clocked_in_users[user_clock_in.user_id] = True
            context["users"] = users
            context["clocked_in_users"] = clocked_in_users

        events = Event.objects.filter(user=self.request.user).all()
        context["events"] = events

        # clocked_in = events.filter(event_type="clock_in", event_from__gte=datetime.now().date()).first()
        # context['clocked_in'] = clocked_in

        return context


class InklokView(LoginRequiredMixin, TemplateView):
    template_name = "inklokken.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(user=self.request.user).all()
        clocked_in = events.filter(
            user=self.request.user,
            event_type="clock_in",
            event_from__gte=datetime.now().date(),
        ).first()
        context["events"] = events
        context["clocked_in"] = clocked_in
        return context


def create_clock_in(request):
    if request.method == "POST":
        form = ClockInForm(request.POST)
        if form.is_valid():
            Event.objects.create(
                description="Ingeklokt voor de werkdag",
                event_type="clock_in",
                event_from=form.cleaned_data["date_from"],
                event_to=form.cleaned_data["date_to"],
                user=request.user,
            )
            messages.success(request, "U heeft succesvol ingeklokt!")
            return HttpResponseRedirect("/inklokken/")

    return HttpResponseRedirect("/inklokken/")


def create_sick_leave(request):
    if request.method == "POST":
        form = SickLeaveForm(request.POST)
        if form.is_valid():
            Event.objects.create(
                description=form.cleaned_data["description"],
                event_type="sick_leave",
                event_from=form.cleaned_data["date_from"],
                event_to=form.cleaned_data["date_to"],
                user=request.user,
            )
            messages.success(request, "Uw ziekmelding is succesvol opgeslagen!")
            return HttpResponseRedirect("/inklokken/")

    return HttpResponseRedirect("/inklokken/")
