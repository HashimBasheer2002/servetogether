import razorpay
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Volunteer, Task, Resource, Feedback, HelpRequest, VolunteerApplication, Role, Profile, FoodDonation, \
    OtherDonation, DisasterReport, Campaign, ResourceUsage, UsedResource
from .serializers import VolunteerSerializer, TaskSerializer, ResourceSerializer, FeedbackSerializer
from .forms import VolunteerApplicationForm, FoodDonationForm, MoneyDonationForm, BloodDonationForm, OtherDonationForm, \
    CampaignForm, VolunteerProfileForm, UsedResourceForm, CertificationForm
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import BloodDonation
from django.conf import settings
from django.shortcuts import  redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
import requests


def about(request):
    return render(request,'about.html')

# Home view to display feedbacks
def home(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'home.html', {'feedbacks': feedbacks})

# API views for handling volunteers, tasks, resources, and feedback
@api_view(['GET', 'POST'])
def volunteer_list(request):
    if request.method == 'GET':
        volunteers = Volunteer.objects.all()
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def certify_volunteer(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)

    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            volunteer.certified = True
            form.save()
            messages.success(request, f"{volunteer.name} is now certified!")
            return redirect('volunteer_list')  # Redirect to volunteer listing page
    else:
        form = CertificationForm(instance=volunteer)

    return render(request, 'certify_volunteer.html', {'form': form, 'volunteer': volunteer})

@login_required
def generate_volunteer_pdf(request):
    volunteers = Volunteer.objects.all()

    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
    pdf_canvas.setFont("Helvetica", 12)
    y = 800

    pdf_canvas.drawString(200, 820, "Volunteer List")
    pdf_canvas.line(50, 810, 550, 810)

    for volunteer in volunteers:
        pdf_canvas.drawString(50, y, f"Name: {volunteer.name}, Phone: {volunteer.contact_details},location:{volunteer.location}")
        y -= 20

        # Page overflow check
        if y < 50:
            pdf_canvas.showPage()
            y = 800

    pdf_canvas.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')






@api_view(['GET', 'POST'])
def resource_list(request):
    if request.method == 'GET':
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def feedback_list(request):
    if request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('feedback_list')  # Redirect after form submission
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    feedbacks = Feedback.objects.all()
    volunteers = Volunteer.objects.all()
    tasks = Task.objects.all()
    return render(request, 'feedback.html', {
        'feedbacks': feedbacks,
        'volunteers': volunteers,
        'tasks': tasks,
    })


# Helper functions to check user roles
def is_admin(user):
    return user.is_staff

def is_volunteer(user):
    return hasattr(user, 'profile') and user.profile.role.name == 'Volunteer'

def is_donor(user):
    return hasattr(user, 'profile') and user.profile.role.name == 'Donor'

def is_user(user):
    return hasattr(user, 'profile') and user.profile.role.name == 'User'

# Volunteer application view
@login_required
def volunteer_application(request):
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST, request.FILES)  # Include request.FILES for file upload
        if form.is_valid():
            # Save the form but don't commit to the database yet
            application = form.save(commit=False)

            # Associate the current logged-in user with the application
            application.user = request.user

            # Now save the application with the user and the uploaded CV
            application.save()

            # Redirect or render the success page
            return render(request, 'application_suucess.html')  # Fix typo in filename
    else:
        form = VolunteerApplicationForm()

    return render(request, 'volunteer_application.html', {'form': form})

# Admin view to see all volunteer applications
@login_required
@user_passes_test(is_admin)
def view_applications(request):
    applications = VolunteerApplication.objects.all().order_by('-applied_at')
    return render(request, 'view_applications.html', {'applications': applications})

# Admin view to update the application status

from django.contrib.auth.models import User  # Assuming you are using the default User model

@login_required
@user_passes_test(is_admin)
def update_application_status(request, application_id, status):
    application = get_object_or_404(VolunteerApplication, id=application_id)

    if status in ['Accepted', 'Rejected']:
        if status == 'Accepted':
            # Update the application's status to "Accepted"
            application.status = 'Accepted'
            application.save()

            # Fetch or create the "Volunteer" role (assuming Role is a model)
            volunteer_role, created = Role.objects.get_or_create(name='Volunteer')

            # Check if a volunteer with the same name already exists
            if not Volunteer.objects.filter(email=application.email).exists():
                volunteer = Volunteer.objects.create(
                    name=application.name,
                    location=application.location,
                    skills=application.certifications,  # Treat certifications as skills
                    availability=True,  # Default availability to True
                    role=volunteer_role,  # Assign the "Volunteer" role
                    contact_details=application.contact_details,
                    email=application.email,
                    profile_picture=application.profile_picture
                )

                # Now update the user role to "Volunteer" (assuming you're using the default User model)
                user = User.objects.get(email=application.email)
                user.profile.role = volunteer_role  # Assuming user profile has a role field
                user.profile.save()

            # Redirect to the view volunteers page
            return redirect('view_volunteers')

        elif status == 'Rejected':
            # If the application is rejected, delete it
            application.delete()

            # Redirect to the applications page after rejection
            return redirect('view_applications')

@login_required
def view_volunteers(request):
    volunteers = Volunteer.objects.all().order_by('name')
    return render(request, 'view_volunteers.html', {'volunteers': volunteers})

# Submit help request (for Donors and Volunteers)
@user_passes_test(is_admin)
def delete_volunteer(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    volunteer.delete()
    messages.success(request, f'Volunteer {volunteer.name} has been deleted successfully.')
    return redirect('volunteer_list')
def submit_help_request(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        location = request.POST.get('location')
        contact_details = request.POST.get('contact_details')
        essentials = request.POST.get('essentials')

        # Create the HelpRequest object
        HelpRequest.objects.create(
            user=request.user,
            description=description,
            location=location,
            contact_details=contact_details,
            essentials=essentials
        )
        messages.success(request, "Your help request has been submitted successfully!")
        return redirect('home')

    return render(request, 'help.html')


def help_requests(request):
    if request.user.is_staff:
        # Admin view for all help requests
        pending_requests = HelpRequest.objects.filter(status='Pending')
        accepted_requests = HelpRequest.objects.filter(status='In Progress').exclude(status='Task')
        return render(request, 'view_help.html', {
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests
        })
    else:
        # Regular user view for their own help requests
        user_requests = HelpRequest.objects.filter(user=request.user)
        return render(request, '', {
            'user_requests': user_requests
        })

def accept_help_request(request, pk):
    if request.user.is_staff:
        help_request = HelpRequest.objects.get(pk=pk)
        help_request.status = 'In Progress'
        help_request.save()
        messages.success(request, "Help request accepted successfully!")
        return redirect('help_requests')  # Redirect to the admin help requests page
    return redirect('home')  # If not admin, redirect to home

def decline_help_request(request, pk):
    if request.user.is_staff:
        help_request = HelpRequest.objects.get(pk=pk)
        help_request.status = 'Declined'
        help_request.save()
        messages.warning(request, "Help request declined!")
        return redirect('help_requests')  # Redirect to the admin help requests page
    return redirect('home')



def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will now automatically assign the "Donor" role
            login(request, user)  # Log in the user after registration
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
# User Login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Using .get() instead of direct access
        password = request.POST.get('password')  # to avoid KeyError

        if username and password:  # Check if both fields are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # or any other page after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Both fields are required.")
    return render(request, 'login.html')

# User Logout
def logout_user(request):
    logout(request)
    return redirect('login')




def donate_resources(request, donation_type=None):
    # If donation_type is not provided, render the page where the user can choose the donation type
    if not donation_type:
        return render(request, 'Donation.html')  # This page lets users choose donation type (blood, food, etc.)

def donate_blood(request):
    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your success URL
    else:
        form = BloodDonationForm()

    return render(request, 'donate_blood.html', {'form': form})



@staff_member_required
def delete_blood_donation(request, donation_id):
    # Get the blood donation by ID
    donation = get_object_or_404(BloodDonation, id=donation_id)

    # Delete the donation
    donation.delete()

    # Redirect to the blood donations list page (or any other page)
    return redirect('home')
def donate_food(request):
    if request.method == 'POST':
        form = FoodDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your success URL
    else:
        form = FoodDonationForm()

    return render(request, 'food.html', {'form': form})





def donate_other(request):
    if request.method == 'POST':
        form = OtherDonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your success URL
    else:
        form = OtherDonationForm()

    return render(request, 'other.html', {'form': form})




def blood_donations_view(request):

    donations = BloodDonation.objects.all()

    return render(request, 'Bloodbank.html', {'donations': donations})


def resource_view(request):
    available_food_donations = FoodDonation.objects.filter(collected=False)
    available_other_donations = OtherDonation.objects.filter(collected=False)

    collected_food_donations = FoodDonation.objects.filter(collected=True)
    collected_other_donations = OtherDonation.objects.filter(collected=True)

    collected_resources = [
        {
            'type': 'Food',
            'description': donation.food_type,
            'quantity': donation.food_quantity,
            'contact_name': donation.contact_name,
            'collected_date': donation.collected_date
        }
        for donation in collected_food_donations
    ] + [
        {
            'type': 'Other',
            'description': donation.resource_description,
            'quantity': donation.resource_quantity,
            'contact_name': donation.contact_name,
            'collected_date': donation.collected_date
        }
        for donation in collected_other_donations
    ]

    return render(request, 'resource.html', {
        'available_food_donations': available_food_donations,
        'available_other_donations': available_other_donations,
        'collected_resources': collected_resources


    })


def mark_collected_food(request, donation_id):
    donation = get_object_or_404(FoodDonation, id=donation_id)
    donation.collected = True
    donation.collected_date = now()
    donation.save()
    return redirect('resources')


def mark_collected_other(request, donation_id):
    donation = get_object_or_404(OtherDonation, id=donation_id)
    donation.collected = True
    donation.collected_date = now()
    donation.save()
    return redirect('resources')



def add_used_resource(request):
    if request.method == "POST":
        form = UsedResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('used_resources_list')
    else:
        form = UsedResourceForm()
    return render(request, 'used_report.html', {'form': form})

def used_resources_list(request):
    resources = UsedResource.objects.all()
    return render(request, 'view_used_report.html', {'resources': resources})


#alert
def report(request):
    return render(request, 'report.html')



import requests

import requests

def reverse_geocode(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'aura-disaster-report/1.0 (auraapp2024@gmail.com)'  # Update to your contact if needed
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('display_name', f"Lat: {lat}, Lng: {lon}")
    return f"Lat: {lat}, Lng: {lon}"

def send_alert(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        phone_number = request.POST['phone_number']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        # Convert lat/lng to address
        location = reverse_geocode(latitude, longitude)

        # Save the report to the database
        report = DisasterReport(
            name=name,
            description=description,
            location=location,
            phone_number=phone_number
        )
        report.save()

        # Email content
        email_subject = 'New Disaster Report Received'
        email_message = (
            f"Name: {name}\n"
            f"Description: {description}\n"
            f"Location: {location}\n"
            f"Contact: {phone_number if phone_number else 'N/A'}"
        )

        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        return render(request, 'success.html')

    return render(request, 'reported.html')


from django.shortcuts import render
from .models import HelpRequest

def send_to_task(request, pk):
    help_request = get_object_or_404(HelpRequest, pk=pk)
    help_request.status = 'Task'  # Set a custom status to indicate it's sent to tasks
    help_request.save()
    return redirect('help_requests')  # Redirect back to the admin page or accepted list

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import HelpRequest

def task_list(request):
    """Displays all tasks categorized as active, awaiting approval, and completed."""
    tasks = HelpRequest.objects.filter(status__in=['Pending', 'In Progress', 'Task'])  # Include 'Task' status
    awaiting_approval_tasks = HelpRequest.objects.filter(status='Awaiting Approval')
    completed_tasks = HelpRequest.objects.filter(status='Completed')

    return render(request, 'task.html', {
        'tasks': tasks,
        'awaiting_approval_tasks': awaiting_approval_tasks,  # Admin section
        'completed_tasks': completed_tasks
    })


import logging

logger = logging.getLogger(__name__)

@login_required
def request_task_completion(request, pk):
    """Allows volunteers to request task completion."""
    task = get_object_or_404(HelpRequest, pk=pk)

    logger.info(f"User {request.user} attempting to request completion for task {pk}")

    if request.method == "POST":
        if task.status in ['Pending', 'In Progress', 'Task']:
            task.status = 'Awaiting Approval'
            task.save()
            messages.success(request, "Task completion request sent to admin.")
            logger.info(f"Task {pk} marked as Awaiting Approval")
        else:
            messages.warning(request, "Task cannot be marked for approval.")
            logger.warning(f"Task {pk} not eligible for approval")

    return redirect('task_list')



@staff_member_required  # Ensures only admin can approve completion
def approve_task_completion(request, pk):
    """Allows admin to approve completion requests."""
    task = get_object_or_404(HelpRequest, pk=pk)

    if task.status == 'Awaiting Approval':
        task.status = 'Completed'
        task.save()
        messages.success(request, "Task has been marked as completed.")
    else:
        messages.warning(request, "Task is not awaiting approval.")

    return redirect('task_list')

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_task_list(request):
    awaiting_approval_tasks = HelpRequest.objects.filter(status='Awaiting Approval')
    return render(request, 'admin_tasks.html', {'awaiting_approval_tasks': awaiting_approval_tasks})

@login_required
@user_passes_test(is_admin)
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Campaign created successfully!")
            return redirect('campaign_list')  # Redirect to a list of campaigns
    else:
        form = CampaignForm()
    return render(request, 'create_campaign.html', {'form': form})

def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaign_list.html', {'campaigns': campaigns})



@login_required
def join_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.user not in campaign.volunteers.all():
        campaign.volunteers.add(request.user)
    return redirect('campaign_list')

@login_required
def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    volunteers = campaign.volunteers.all()
    return render(request, 'campaign_detail.html', {'campaign': campaign, 'volunteers': volunteers})

@login_required
@user_passes_test(is_admin)
def delete_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    campaign.delete()
    messages.success(request, "Campaign successfully deleted.")
    return redirect('campaign_list')



@login_required
def volunteer_profile_view(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    context = {'volunteer': volunteer}
    return render(request, 'view_profile.html', context)


@login_required
def volunteer_profile_update(request):
    volunteer = get_object_or_404(Volunteer, email=request.user.email)

    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('view_volunteer_profile', id=volunteer.id)
    else:
        form = VolunteerProfileForm(instance=volunteer)

    return render(request, 'volunteer_profile.html', {'form': form, 'volunteer': volunteer})


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def donate_cash(request):
    if request.method == "POST":
        # Create an order in Razorpay
        amount = int(request.POST.get('amount')) * 100  # Convert to paise
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'

        payment_order = client.order.create({
            'amount': amount,
            'currency': order_currency,
            'receipt': order_receipt
        })

        payment_order_id = payment_order['id']

        context = {
            'amount': amount,
            'order_id': payment_order_id,
            'key_id': settings.RAZORPAY_KEY_ID
        }

        return render(request, 'cash.html', context)

    return render(request, 'cash.html')


@csrf_exempt
def payment_success(request):
    return render(request, 'payment_success.html')


