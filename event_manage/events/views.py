from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Event, RSVP
from django.urls import reverse
from django.contrib import messages
def is_admin(user):
    return user.is_staff

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on user role
            if user.is_superuser:
                print("Redirecting to admin panel")
                return redirect('event_list')
            else:
                return redirect('event_list')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

@login_required
def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})



@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    try:
        rsvp = RSVP.objects.get(event=event, user=request.user)
    except RSVP.DoesNotExist:
        rsvp = None

    if request.method == 'POST':
        status = request.POST.get('status')
        if event.date < timezone.now().date():
            return render(request, 'events/event_detail.html', {
                'event': event,
                'rsvp': rsvp,
                'error': "Cannot RSVP to past events."
            })

        if status not in ['going', 'maybe', 'declined']:
            return render(request, 'events/event_detail.html', {
                'event': event,
                'rsvp': rsvp,
                'error': "Invalid RSVP status."
            })

        if rsvp:
            rsvp.status = status
            rsvp.save()
        else:
            RSVP.objects.create(event=event, user=request.user, status=status)

        return redirect('my_rsvps')

    return render(request, 'events/event_detail.html', {'event': event, 'rsvp': rsvp})

@login_required
def my_rsvps(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event').order_by('event__date')
    return render(request, 'events/my_rsvps.html', {'rsvps': rsvps})

# Admin-only views for CRUD on events

@login_required

def admin_event_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')

        # Basic validation
        if not all([title, description, date, start_time, end_time, location]):
            return render(request, 'events/admin_event_form.html', {'error': 'All fields are required.'})

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            created_by=request.user
        )
        return redirect('event_list')

    return render(request, 'events/admin_event_form.html')

@login_required
@user_passes_test(is_admin)
def admin_event_update(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.location = request.POST.get('location')

        if not all([event.title, event.description, event.date, event.start_time, event.end_time, event.location]):
            return render(request, 'events/admin_event_form.html', {'event': event, 'error': 'All fields are required.'})

        event.save()
        return redirect('event_list')

    return render(request, 'events/admin_event_form.html', {'event': event})

@login_required
@user_passes_test(is_admin)
def admin_event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return render(request, 'events/admin_event_confirm_delete.html', {'event': event})

@login_required
@user_passes_test(is_admin)
def admin_event_rsvp_summary(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    going_count = RSVP.objects.filter(event=event, status='going').count()
    maybe_count = RSVP.objects.filter(event=event, status='maybe').count()
    declined_count = RSVP.objects.filter(event=event, status='declined').count()

    return render(request, 'events/admin_event_rsvp_summary.html', {
        'event': event,
        'going_count': going_count,
        'maybe_count': maybe_count,
        'declined_count': declined_count,
    })



from .forms import CustomSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  

    else:
        form = CustomSignupForm()
    return render(request, 'events/signup.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('login')

