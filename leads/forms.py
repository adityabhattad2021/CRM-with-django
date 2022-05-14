from django import forms
from .models import Lead,Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UsernameField

User=get_user_model()

class createLeadForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields=(
            'first_name',
            'last_name',
            'age',
            'agent',
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=("username",)
        fields_classes={'username':UsernameField}



class AssignAgentForm(forms.Form):
    agent=forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self,*args,**kwargs):
        # print("In Form")
        request=kwargs.pop('request')
        agents=Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args,**kwargs)
        self.fields["agent"].queryset=agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model=Lead
        fields=(
            'category',
        )


