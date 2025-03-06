from django.urls import path
from . import views
from .views import volunteer_application, update_application_status, view_applications, view_volunteers, \
    certify_volunteer

urlpatterns = [
    # Home page URL pattern (API base)
    path('api/', views.home, name='home'),

    # Volunteer-related views
    path('api/volunteers/', views.view_volunteers, name='volunteer_list'),
    path('volunteers/pdf/', views.generate_volunteer_pdf, name='volunteer_pdf'),
    path('api/resources/', views.resource_list, name='resource_list'),
    path('api/feedback/', views.feedback_list, name='feedback_list'),

    # Help request submission
    path('help/submit/', views.submit_help_request, name='submit_help_request'),

    # Volunteer application and admin views
    path('apply/', volunteer_application, name='volunteer_application'),
    path('applications/', view_applications, name='view_applications'),
    path('applications/<int:application_id>/<str:status>/', update_application_status, name='update_application_status'),
    path('volunteer/delete/<int:volunteer_id>/', views.delete_volunteer, name='delete_volunteer'),

    # Authentication URLs
    path('register/', views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    #volunteers list
    path('volunteers/', views.view_volunteers, name='view_volunteers'),

    #help reuest view and accept
    path('help-requests/', views.help_requests, name='help_requests'),
    path('help-request/accept/<int:pk>/', views.accept_help_request, name='accept_help_request'),

#donation

    path('donate/blood/', views.donate_blood, name='donate_blood'),
    path('donate_blood/delete/<int:donation_id>/', views.delete_blood_donation, name='delete_blood_donation'),
    path('donate/food/', views.donate_food, name='donate_food'),
    path('donate/other/', views.donate_other, name='donate_other'),
    path('donate/', views.donate_resources, name='donate_resources'),
    path('resources',views.resource_view,name='resources'),

    #bloodbank
    path('bloodbank/', views.blood_donations_view, name='bloodbank'),


#resource view


    #report disaster
    path('report/', views.report, name='report'),
    path('send-alert/', views.send_alert, name='send_alert'),
    # Optional success page
    path('about/', views.about, name='about'),

#task
    path('tasks/', views.task_list, name='task_list'),
    path('send-to-task/<int:pk>/', views.send_to_task, name='send_to_task'),
    path('tasks/<int:pk>/completed/', views.mark_task_completed, name='mark_task_completed'),

    path('mark_collected_food/<int:donation_id>/', views.mark_collected_food, name='mark_collected_food'),
    path('mark_collected_other/<int:donation_id>/', views.mark_collected_other, name='mark_collected_other'),


#campaign
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('join-campaign/<int:campaign_id>/', views.join_campaign, name='join_campaign'),
    path('campaign-detail/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/delete/<int:pk>/', views.delete_campaign, name='delete_campaign'),

#profile
    path('volunteer-profile/<int:id>/', views.volunteer_profile_view, name='view_volunteer_profile'),
    path('volunteer-profile/update/', views.volunteer_profile_update, name='update_volunteer_profile'),

    path('donate_cash/', views.donate_cash, name='donate_cash'),
    path('payment_success/', views.payment_success, name='payment_success'),

    path('add-used-resource/', views.add_used_resource, name='add_used_resource'),
    path('used-resources/', views.used_resources_list, name='used_resources_list'),
    path('certify/<int:volunteer_id>/', certify_volunteer, name='certify_volunteer'),



]




