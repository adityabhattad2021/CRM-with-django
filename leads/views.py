from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.urls import reverse
from .models import Lead,Category
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView,FormView
from .forms import createLeadForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisationAndLoginRequiredMixin



# Create your views here.
class HomePageView(TemplateView):
    template_name='main.html'

class SignUpView(CreateView):
    template_name='registration/signup.html'
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse('login-page')


class LeadListView(LoginRequiredMixin, ListView):
    template_name='leads/all_leads.html'
    context_object_name='leads'

    def get_queryset(self):
        user=self.request.user

        # Initial queryset of leads for entire organisation
        if user.is_organisor:
            queryset=Lead.objects.filter(organistaion=user.userprofile,agent__isnull=False)
            # print(queryset)
        else:
            queryset=Lead.objects.filter(organistaion=user.agent.organisation,agent__isnull=False)
            # Filter for the Logged-in Agent
            queryset=Lead.objects.filter(agent__user=user)

        return queryset
    
    def get_context_data(self, **kwargs):
        user=self.request.user

        context=super(LeadListView,self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset=Lead.objects.filter(
                organistaion=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context




class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name='leads/lead.html'

    context_object_name='lead'

    def get_queryset(self):
        user=self.request.user

        # Initial queryset of leads for entire organisation
        if user.is_organisor:
            queryset=Lead.objects.filter(organistaion=user.userprofile)
        else:
            queryset=Lead.objects.filter(organistaion=user.agent.organisation)
            # Filter for the Logged-in Agent
            queryset=Lead.objects.filter(agent__user=user)

        return queryset


class LeadCreateView(OrganisationAndLoginRequiredMixin, CreateView):
    template_name='leads/create_lead.html'
    form_class=createLeadForm

    def get_success_url(self):
        return reverse('leads:leads-page')


    def form_valid(self,form):
        lead=form.save(commit=False)
        lead.organistaion=self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A new lead has been created",
            message="Go to the site to ckeck the lead",
            from_email='test@test.com',
            recipient_list=["test2@test.com"],
        )
        return super(LeadCreateView,self).form_valid(form)



class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name='leads/update_lead.html'

    form_class=createLeadForm

    def get_queryset(self):
        user=self.request.user
        # Initial queryset of leads for entire organisation
        queryset=Lead.objects.filter(organistaion=user.userprofile)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-page',kwargs={"pk":self.get_object().id})


class LeadDeleteView(OrganisationAndLoginRequiredMixin, DeleteView):
    template_name='leads/delete_lead.html'

    def get_queryset(self):
        user=self.request.user
        # Initial queryset of leads for entire organisation
        queryset=Lead.objects.filter(organistaion=user.userprofile)
        return queryset


    def get_success_url(self):
        return reverse("leads:leads-page")


class AssignAgentView(OrganisationAndLoginRequiredMixin,FormView):
    template_name='leads/assign_agent.html'
    form_class=AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request':self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leads-page")

    def form_valid(self,form):
        agent=form.cleaned_data["agent"]
        lead=Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)


class CategoryListView(LoginRequiredMixin,ListView):
    template_name="leads/catogery_list.html"
    context_object_name= "catogery_list"

    def get_context_data(self,**kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        user=self.request.user

        if user.is_organisor:
            queryset=Lead.objects.filter(
                organistaion=user.userprofile
            )
        else:
            queryset=Lead.objects.filter(
                organistaion=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count()
        })
        return context


    def get_queryset(self):
        user=self.request.user

        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset



class CategoryDetailView(LoginRequiredMixin,DetailView):
    template_name="leads/category-details.html"
    context_object_name='category'

    def get_queryset(self):
        user=self.request.user

        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)

        return queryset


    def get_context_data(self,**kwargs):
        context=super(CategoryDetailView,self).get_context_data(**kwargs)
        leads=self.get_object().leads.all()
        context.update({
            'leads':leads
        })
        return context


class LeadCategoryUpdateView(LoginRequiredMixin,UpdateView):
    template_name="leads/lead_category_update.html"
    form_class=LeadCategoryUpdateForm

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organistaion=user.userprofile)
        else:
            queryset=Lead.objects.filter(organistaion=user.agent.organisation)
            queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse('leads:lead-page',kwargs={"pk":self.get_object().id})
    

# Function Based Views.
# def updateleadView(request,pk):
#     lead=Lead.objects.get(id=pk)
#     form=createLeadForm(instance=lead)
#     if request.method=='POST':
#         form=createLeadForm(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('leads:leads-page')
#     context={
#         'form':form,
#         'lead':lead
#     }
#     return render(request,'leads/update_lead.html',context)


# def deleteleadView(request,pk):
#     lead=Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect('leads:leads-page')



# def mainView(request):
#     return render(request,'leads/main.html')


# def LeadsView(request):
#     leads=Lead.objects.all()
#     context={
#         'leads':leads,
#     }
#     return render(request,'leads/all_leads.html',context)


# def createleadView(request):
#     form=createLeadForm()
#     if request.method=='POST':
#         form=createLeadForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('leads:leads-page')
#     context={
#         'form':form,
#     }
#     return render(request,'leads/create_lead.html',context)


# def LeadView(request,pk):
#     lead=Lead.objects.get(id=pk)
#     context={
#         'lead':lead
#     }
#     return render(request,'leads/lead.html',context)
