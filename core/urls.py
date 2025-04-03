from django.urls import path
from . import views
from .views import volunteer_application, update_application_status, view_applications, view_volunteers, \
    certify_volunteer, request_task_completion, approve_task_completion, admin_task_list
from django.contrib.auth import views as auth_views


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

    path('send-to-task/<int:pk>/', views.send_to_task, name='send_to_task'),
    path('task/request_complete/<int:pk>/', request_task_completion, name='request_task_completion'),
    path('task/approve/<int:pk>/', approve_task_completion, name='approve_task_completion'),
    path('tasks/', views.task_list, name='task_list'),  # Regular task list
    path('admintask/', views.admin_task_list, name='admin_task_list'),  # Admin-only view

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

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]




