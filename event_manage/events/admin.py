from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'location', 'created_by')
    list_filter = ('date', 'location', 'created_by')
    search_fields = ('title', 'description', 'location', 'created_by__username')
    ordering = ('-date',)
    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
            obj.created_by = request.user
        obj.save()

    def has_add_permission(self, request):
        return request.user.is_staff  # Only admins can add

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Only admins can edit

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Only admins can delete

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('event__title', 'user__username')
    ordering = ('-updated_at',)