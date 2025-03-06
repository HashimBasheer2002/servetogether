from django.contrib import admin
from .models import Volunteer, Task, Resource, Feedback, HelpRequest, VolunteerApplication, Role, Profile, \
    BloodDonation, FoodDonation, MoneyDonation, OtherDonation, ResourceUsage


# Registering the Role model
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Role, RoleAdmin)

# Registering the Volunteer model
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'availability', 'role')
    search_fields = ('name', 'location')
    list_filter = ('role', 'availability')

admin.site.register(Volunteer, VolunteerAdmin)

# Registering the Task model
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_volunteer', 'deadline')
    search_fields = ('name', 'assigned_volunteer__name')
    list_filter = ('assigned_volunteer', 'deadline')

admin.site.register(Task, TaskAdmin)

# Registering the Resource model
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'allocated_to_task')
    search_fields = ('name',)
    list_filter = ('allocated_to_task',)

admin.site.register(Resource, ResourceAdmin)

# Registering the Feedback model
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'task', 'comments')
    search_fields = ('volunteer__name', 'task__name')
    list_filter = ('task',)

admin.site.register(Feedback, FeedbackAdmin)

# Registering the HelpRequest model
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    search_fields = ('user__username', 'status')
    list_filter = ('status',)

admin.site.register(HelpRequest, HelpRequestAdmin)

# Registering the VolunteerApplication model
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'applied_at')
    search_fields = ('name', 'location', 'email')
    list_filter = ('status', 'role')

admin.site.register(VolunteerApplication, VolunteerApplicationAdmin)

# Registering the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'address')
    search_fields = ('user__username',)
    list_filter = ('role',)

admin.site.register(Profile, ProfileAdmin)


admin.site.register(BloodDonation)

admin.site.register(FoodDonation)

admin.site.register(MoneyDonation)

admin.site.register(OtherDonation)


admin.site.register(ResourceUsage)



class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'certified')
    list_filter = ('certified',)
    search_fields = ('name', 'email')
    actions = ['certify_volunteers']

    def certify_volunteers(self, request, queryset):
        queryset.update(certified=True)
    certify_volunteers.short_description = "Mark selected volunteers as certified"




