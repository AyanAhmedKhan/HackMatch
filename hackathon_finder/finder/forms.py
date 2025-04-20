from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Message, Skill, TechStack, Hackathon

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    new_skills = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type skills separated by commas',
            'class': 'tag-input'
        }),
        help_text="Add new skills by typing them (comma separated)"
    )

    new_tech_stack = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type technologies separated by commas',
            'class': 'tag-input'
        }),
        help_text="Add new technologies by typing them (comma separated)"
    )

    hackathon_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Hackathon name',
            'class': 'hackathon-input'
        })
    )

    hackathon_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Brief description',
            'class': 'hackathon-desc'
        })
    )

    hackathon_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="When did you participate?"
    )

    hackathon_role = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your role/achievement',
            'class': 'hackathon-role'
        })
    )

    hackathon_level = forms.ChoiceField(
        choices=Hackathon.LEVEL_CHOICES,
        required=False,
        label='Hackathon Level'
    )

    hackathon_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Hackathon location',
            'class': 'hackathon-input'
        })
    )

    class Meta:
        model = Profile
        fields = (
            'bio', 'location', 'skills', 'tech_stack', 'interested_hackathons',
            'profile_picture', 'looking_for_team', 'college', 'branch'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
            'tech_stack': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
            'interested_hackathons': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
            'looking_for_team': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
        labels = {
            'looking_for_team': 'Actively looking for team members',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].required = False
        self.fields['tech_stack'].required = False
        self.fields['interested_hackathons'].required = False

    def save(self, commit=True):
        profile = super().save(commit=False)

        if commit:
            profile.save()
            self.save_m2m()

            # Process new skills
            new_skills = self.cleaned_data.get('new_skills', '')
            if new_skills:
                for skill_name in [s.strip() for s in new_skills.split(',') if s.strip()]:
                    skill, created = Skill.objects.get_or_create(name=skill_name.lower())
                    profile.skills.add(skill)

            # Process new tech stack
            new_tech_stack = self.cleaned_data.get('new_tech_stack', '')
            if new_tech_stack:
                for tech_name in [t.strip() for t in new_tech_stack.split(',') if t.strip()]:
                    tech, created = TechStack.objects.get_or_create(name=tech_name.lower())
                    profile.tech_stack.add(tech)

            # Process new hackathon
            hackathon_name = self.cleaned_data.get('hackathon_name')
            if hackathon_name:
                hackathon, created = Hackathon.objects.get_or_create(
                    name=hackathon_name,
                    defaults={
                        'description': self.cleaned_data.get('hackathon_description', ''),
                        'start_date': self.cleaned_data.get('hackathon_date'),
                        'end_date': self.cleaned_data.get('hackathon_date'),
                        'location': self.cleaned_data.get('hackathon_location') or 'Online',
                        'level': self.cleaned_data.get('hackathon_level') or 'other'
                    }
                )
                profile.interested_hackathons.add(hackathon)

        return profile


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


class ProfileSearchForm(forms.Form):
    search = forms.CharField(required=False)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    location = forms.CharField(required=False)
    hackathon = forms.ModelChoiceField(
        queryset=Hackathon.objects.all(),
        required=False,
        empty_label="Any Hackathon"
    )
    looking_for_team = forms.BooleanField(
        required=False,
        label='Only show profiles looking for team members'
    )
    college = forms.CharField(
        required=False,
        label='Filter by college/university'
    )



















# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Profile, Message, Skill, TechStack, Hackathon

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

# class ProfileForm(forms.ModelForm):
#     new_skills = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Type skills separated by commas',
#             'class': 'tag-input'
#         }),
#         help_text="Add new skills by typing them (comma separated)"
#     )
    
#     new_tech_stack = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Type technologies separated by commas',
#             'class': 'tag-input'
#         }),
#         help_text="Add new technologies by typing them (comma separated)"
#     )
    
#     hackathon_name = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Hackathon name',
#             'class': 'hackathon-input'
#         })
#     )
    
#     hackathon_description = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'rows': 2,
#             'placeholder': 'Brief description',
#             'class': 'hackathon-desc'
#         })
#     )
    
#     hackathon_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         help_text="When did you participate?"
#     )
    
#     hackathon_role = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Your role/achievement',
#             'class': 'hackathon-role'
#         })
#     )
    
#     hackathon_level = forms.ChoiceField(
#         choices=Hackathon.LEVEL_CHOICES,
#         required=False,
#         label='Hackathon Level'
#     )
    
#     hackathon_location = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Hackathon location',
#             'class': 'hackathon-input'
#         })
#     )
    
    

#     class Meta:
#         model = Profile
#         fields = ('bio', 'location', 'skills', 'tech_stack', 'interested_hackathons', 
#                   'profile_picture', 'looking_for_team', 'college', 'branch', 
#                   'hackathon_name', 'hackathon_description', 'hackathon_date', 
#                   'hackathon_role', 'hackathon_level', 'hackathon_location')  # Add hackathon_location here
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 4}),
#             'skills': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
#             'tech_stack': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
#             'interested_hackathons': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
#             'looking_for_team': forms.CheckboxInput(attrs={'class': 'checkbox'}),
#         }
#         labels = {
#             'looking_for_team': 'Actively looking for team members',
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['skills'].required = False
#         self.fields['tech_stack'].required = False
#         self.fields['interested_hackathons'].required = False

#     def save(self, commit=True):
#         instance = super().save(commit=False)
        
#         # Process new skills
#         new_skills = self.cleaned_data.get('new_skills', '')
#         if new_skills:
#             for skill_name in [s.strip() for s in new_skills.split(',') if s.strip()]:
#                 skill, created = Skill.objects.get_or_create(name=skill_name.lower())
#                 instance.skills.add(skill)
        
#         # Process new tech stack items
#         new_tech_stack = self.cleaned_data.get('new_tech_stack', '')
#         if new_tech_stack:
#             for tech_name in [t.strip() for t in new_tech_stack.split(',') if t.strip()]:
#                 tech, created = TechStack.objects.get_or_create(name=tech_name.lower())
#                 instance.tech_stack.add(tech)
        
#         # Process new hackathon
#         hackathon_name = self.cleaned_data.get('hackathon_name')
#         if hackathon_name:
#             hackathon, created = Hackathon.objects.get_or_create(
#                 name=hackathon_name,
#                 defaults={
#                     'description': self.cleaned_data.get('hackathon_description', ''),
#                     'start_date': self.cleaned_data.get('hackathon_date'),
#                     'end_date': self.cleaned_data.get('hackathon_date'),
#                     'location': 'Online',
#                     'level': self.cleaned_data.get('hackathon_level', 'other')
#                 }
#             )
#             instance.interested_hackathons.add(hackathon)
        
#         if commit:
#             instance.save()
#             self.save_m2m()
        
#         return instance
#     #testind this -----------------------------------------------------------------------------------------------
#     def save(self, commit=True):
#         profile = super().save(commit=False)
        
#         if commit:
#             profile.save()
#             self.save_m2m()  # This will save the many-to-many data from the form
            
#         return profile

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ('content',)
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 4}),
#         }

# class ProfileSearchForm(forms.Form):
#     search = forms.CharField(required=False)
#     skills = forms.ModelMultipleChoiceField(
#         queryset=Skill.objects.all(),
#         required=False,
#         widget=forms.CheckboxSelectMultiple
#     )
#     location = forms.CharField(required=False)
#     hackathon = forms.ModelChoiceField(
#         queryset=Hackathon.objects.all(),
#         required=False,
#         empty_label="Any Hackathon"
#     )
#     looking_for_team = forms.BooleanField(
#         required=False,
#         label='Only show profiles looking for team members'
#     )
#     college = forms.CharField(
#         required=False,
#         label='Filter by college/university'
#     )