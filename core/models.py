from django.db import models
from django.contrib.auth.models import User




class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    volunteers = models.ManyToManyField(User, related_name='joined_campaigns', blank=True)


    def __str__(self):
        return self.name





class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile',null=True)
    name = models.CharField(max_length=100, default="Enter your Name")
    skills = models.TextField()
    location = models.CharField(max_length=100, null=True)
    availability = models.BooleanField()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    contact_details = models.CharField(max_length=100, null=True)
    profile_picture = models.ImageField(upload_to='static/images/', null=True, blank=True)
    certified = models.BooleanField(default=False)  # Indicates whether the volunteer is certified
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)



def __str__(self):
        return self.name



class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Declined', 'Declined'),  # Optional: Add Declined status
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_requests')
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=100)
    essentials = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help Request by {self.user.username} - {self.status}"




class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_volunteer = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateField()
     # Link to HelpRequest

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    allocated_to_task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comments = models.TextField()

    def __str__(self):
        return f"Feedback by {self.volunteer.name} for {self.task.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    # Add a role field to the profile for user access control
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.user.username



class VolunteerApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=225, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    certifications = models.TextField(blank=True, null=True)
    contact_details = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Application from {self.name}"




from django.db import models

# models.py

from django.db import models

# models.py
# models.py
class BloodDonation(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O-'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    blood_amount = models.DecimalField(max_digits=5, decimal_places=2)
    contact_name = models.CharField(max_length=100, null=True, blank=True)  # Made nullable
    contact_phone = models.CharField(max_length=15,null=True)
    contact_email = models.EmailField(null=True, blank=True)  # Made nullable
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blood Donation ({self.blood_group}) by {self.contact_name} on {self.created_at.strftime('%Y-%m-%d')}"




class MoneyDonation(models.Model):
    money_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Money Donation of {self.money_amount} on {self.created_at.strftime('%Y-%m-%d')}"




class OtherDonation(models.Model):
    resource_description = models.CharField(max_length=100)
    resource_quantity = models.PositiveIntegerField()
    contact_name = models.CharField(max_length=100, null=True)  # New field for donor name
    contact_phone = models.CharField(max_length=15, null=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_address = models.CharField(max_length=200, null=True)
    supply_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_required = models.BooleanField(default=False)
    collected = models.BooleanField(default=False)  # New field
    collected_date = models.DateTimeField(null=True, blank=True)
    # New field for pickup preference
    donation_type = models.CharField(max_length=50, choices=[  # New field for donation type
        ('Furniture', 'Furniture'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Electronics', 'Electronics'),
        ('Other', 'Other'),
    ], default='Other')

    def __str__(self):
        return f"Other Donation ({self.resource_description[:30]}) on {self.created_at.strftime('%Y-%m-%d')}"

class UsedResource(models.Model):
    resource_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    place_used = models.CharField(max_length=300)
    time_used = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_name} - {self.quantity} used at {self.place_used}"


class FoodDonation(models.Model):
    food_type = models.CharField(max_length=50)
    food_quantity = models.PositiveIntegerField()
    contact_name = models.CharField(max_length=100, null=True)
    contact_phone = models.CharField(max_length=15, null=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_address = models.CharField(max_length=200, null=True)
    supply_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    collected = models.BooleanField(default=False)
    collected_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Food Donation ({self.food_type}) on {self.created_at.strftime('%Y-%m-%d')}"


#alert

class DisasterReport(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class ResourceUsage(models.Model):
    RESOURCE_TYPES = [
        ('Blood', 'Blood Donation'),
        ('Money', 'Money Donation'),
        ('Other', 'Other Donation'),
        ('Food', 'Food Donation'),
    ]

    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    donation_id = models.PositiveIntegerField()  # Reference the specific donation
    used_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Supports both quantity and money usage
    usage_description = models.TextField()
    usage_date = models.DateField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)  # Volunteer or Admin who updated this

    def __str__(self):
        return f"Usage of {self.resource_type} (ID: {self.donation_id}) on {self.usage_date}"


