from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Role, VolunteerApplication, HelpRequest, Campaign, Volunteer, ResourceUsage, UsedResource
from .models import BloodDonation, FoodDonation, MoneyDonation, OtherDonation
from .models import Profile, Role
# Custom User Creation Form to include role selection
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Role

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address", "class": "input"}),
        error_messages={
            "required": "Please enter an email address.",
            "invalid": "Please enter a valid email address.",
        },
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder": "Enter your phone number", "class": "input"})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Enter your address", "class": "input", "rows": 3}),
        label="Address"
    )
    # Customize username and password fields
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter your username", "class": "input"}),
        error_messages={
            "required": "Please enter a username.",
            "max_length": "Username must be 150 characters or fewer.",
        },
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "input"}),
        error_messages={"required": "Please provide a password."},
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter your password", "class": "input"}),
        error_messages={"required": "Please confirm your password."},
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']  # Include 'email' in the fields list

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:  # Replace with your custom minimum length
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Assign the default role as "Donor"
        donor_role = Role.objects.get(name='Donor')  # Ensure this role exists in the database
        Profile.objects.create(
            user=user,
            role=donor_role,
            phone=self.cleaned_data.get('phone'),
            address=self.cleaned_data.get('address')
        )
        return user
# Volunteer Application Form
class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['name', 'location', 'gender', 'age', 'qualification', 'certifications', 'contact_details', 'email', 'cv']
        widgets = {
            'certifications': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cv'].required = False  # Make CV optional



# Help Request Form
class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = ['description', 'location', 'contact_details', 'essentials']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'essentials': forms.Textarea(attrs={'rows': 3}),
        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'place', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py


class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = ['blood_group', 'blood_amount', 'contact_name', 'contact_phone', 'contact_email']


class FoodDonationForm(forms.ModelForm):
    class Meta:
        model = FoodDonation
        fields = ['food_type', 'food_quantity', 'contact_name', 'contact_phone', 'contact_email', 'contact_address', 'supply_date']


class MoneyDonationForm(forms.ModelForm):
    class Meta:
        model = MoneyDonation
        fields = ['money_amount']


class OtherDonationForm(forms.ModelForm):
    class Meta:
        model = OtherDonation
        fields = [
            'resource_description', 'resource_quantity', 'contact_name',
            'contact_phone', 'contact_email', 'contact_address',
            'supply_date', 'pickup_required','donation_type'
        ]


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'skills', 'location', 'availability', 'profile_picture', 'contact_details']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }



class UsedResourceForm(forms.ModelForm):
    class Meta:
        model = UsedResource
        fields = ['resource_name', 'quantity', 'place_used']


from django import forms
from .models import Volunteer

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['certified', 'certificate']

