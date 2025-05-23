
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.event_list, name='event_list'),  # List of upcoming events
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Event details + RSVP
    path('my-rsvps/', views.my_rsvps, name='my_rsvps'),  # User's RSVP list
    path('events/create/', views.admin_event_create, name='admin_event_create'),
    path('events/<int:event_id>/update/', views.admin_event_update, name='admin_event_update'),
    path('events/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),
    path('events/<int:event_id>/rsvp-summary/', views.admin_event_rsvp_summary, name='admin_event_rsvp_summary'),


    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),  # You write a simple signup view
    
]