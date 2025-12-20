"""
Forms for the news application.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Article, Newsletter, Publisher


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user with custom fields.
    
    Extends Django's UserCreationForm to include role selection,
    profile information, and custom user fields.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 
                  'first_name', 'last_name', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Simple login form for user authentication.
    
    Collects username and password for user login.
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ArticleForm(forms.ModelForm):
    """
    Form for creating/updating articles.
    
    Allows journalists to create or edit articles with title, content,
    summary, publisher selection, and featured image upload.
    """
    
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'publisher', 'featured_image']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter publishers based on journalist's affiliations
        if user and user.role == 'journalist':
            self.fields['publisher'].queryset = user.affiliated_publishers.all()
            self.fields['publisher'].required = False
            self.fields['publisher'].help_text = 'Select a publisher or leave blank for independent article'


class ArticleApprovalForm(forms.ModelForm):
    """
    Form for editors to approve articles.
    
    Provides a simple checkbox interface for editors to approve
    or reject pending articles submitted by journalists.
    """
    
    class Meta:
        model = Article
        fields = ['is_approved']
        widgets = {
            'is_approved': forms.CheckboxInput(),
        }


class PublisherForm(forms.ModelForm):
    """
    Form for creating/updating publishers.
    
    Allows editors to create or edit publisher organizations with
    name, description, logo, and website information.
    """

    class Meta:
        model = Publisher
        fields = ['name', 'description', 'logo', 'website']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
