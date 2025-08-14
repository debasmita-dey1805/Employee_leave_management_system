from django import forms
from django.contrib.auth.models import User
from .models import Profile

class AddEmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['role']  

    def __init__(self, *args, **kwargs):
        self.manager_department = kwargs.pop('manager_department', None)
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('employee', 'Employee')]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', ''),
            email=self.cleaned_data.get('email', ''),
            password="defaultpassword123"  
        )

        profile = Profile.objects.get(user=user)
        profile.role = self.cleaned_data['role']
        profile.department = self.manager_department

        if commit:
            profile.save()
        return profile
