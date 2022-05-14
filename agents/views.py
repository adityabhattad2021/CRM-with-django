from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse
from leads.models import Agent
from .forms import AgentModelForm,AgentUpdateModelForm
from .mixins import OrganisationAndLoginRequiredMixin
from random import randint


# Create your views here.
class AgentListView(OrganisationAndLoginRequiredMixin,generic.ListView):
    template_name='agents/all_agents.html'
    context_object_name='all_agents'

    def get_queryset(self) :
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisationAndLoginRequiredMixin,generic.CreateView):
    template_name='agents/create_agent.html'
    form_class=AgentModelForm

    def get_success_url(self):
        return reverse("agents:agents-page")

    def form_valid(self,form):
        user=form.save(commit=False)
        # user.organisation=self.request.user.userprofile
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f'{randint(0,1000000)}'),
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )
        return super(AgentCreateView,self).form_valid(form)


class AgentUpdateView(OrganisationAndLoginRequiredMixin,generic.UpdateView):
    template_name='agents/update_agent.html'
    form_class=AgentUpdateModelForm

    def get_queryset(self):
        organisation=self.request.user.userprofile
        agent=Agent.objects.filter(organisation=organisation)
        return agent

    def get_success_url(self):
        return reverse('agents:agents-page')


class AgentDeleteView(OrganisationAndLoginRequiredMixin,generic.DeleteView):
    template_name='agents/delete_agent.html'
    
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

    def get_success_url(self):
        return reverse('agents:agents-page')


class AgentDetailView(OrganisationAndLoginRequiredMixin,generic.DetailView):
    template_name='agents/agent.html'
    context_object_name = "agent"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

