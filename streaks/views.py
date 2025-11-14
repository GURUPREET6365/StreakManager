from django.shortcuts import render, redirect, get_object_or_404
#get_object_or_404: Function to fetch an object from database, or show 404 error if not found
from django.contrib.auth.decorators import login_required
from .models import Streak
 #This will help to take the current time.
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from .forms import StreakForm

@login_required
def create_streaks(request):
    if request.method == 'POST':
        # Get data from the form
        created_date = timezone.localdate()
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Create and save the streak to database Streak.objects: The manager for your Streak model. It handles all database operations
        new_streak = Streak.objects.create(
            user=request.user,
            title=title,
            description=description,
            updated_at=created_date
        )
        
        # Redirect to home page after creating
        return redirect('home')
    
    else:
        # If GET request, just show the empty form
        return render(request, 'streaks/create_streaks.html')

@login_required
def show_streaks(request):
    # Get all streaks for the logged-in user
    '''
    .filter(): Gets multiple objects that match the conditions
    user=request.user: Only get streaks belonging to the logged-in user
    '''
    user_streaks = Streak.objects.filter(user=request.user, is_active=True, is_deleted = False)
    today = timezone.localdate() 
    # Send the streaks to the template
    return render(request, 'streaks/show_streaks.html', {'streaks': user_streaks, 'today': today})


@login_required
def streak_details(request, pk):
    # Get the specific streak by ID, or show 404 if not found
    streak = get_object_or_404(Streak, pk=pk, user=request.user)
    today = timezone.localdate()
    # Send the streak to the template
    return render(request, 'streaks/streak_details.html', {'streak': streak, 'today': today})


@login_required
def streak_update(request, pk):
    if request.method != 'POST':
        return redirect('show_streaks')
    today = timezone.localdate()
    yesterday = today - timedelta(days=1) # This will subtract day 1 from todays date.
    two_days_before = yesterday -timedelta(days=1)
    streak_id = get_object_or_404(Streak, pk=pk, user=request.user)
    last_completed = streak_id.last_completed
    if request.method == 'POST':
        if last_completed is None:
            streak_id.current_streak = 1
            streak_id.longest_streak = max(streak_id.longest_streak, streak_id.current_streak) #: This function compares the two values and returns the one that is larger.
            streak_id.last_completed = today
            streak_id.save()
        elif last_completed == yesterday:
            streak_id.current_streak += 1
            streak_id.longest_streak = max(streak_id.longest_streak, streak_id.current_streak) #: This function compares the two values and returns the one that is larger.
            streak_id.last_completed = today
            streak_id.save()
        elif last_completed == today:
            messages.error(request, "Today target is already completed.")
        elif last_completed <= two_days_before:
            streak_id.current_streak = 1
            streak_id.longest_streak = max(streak_id.longest_streak, streak_id.current_streak) #: This function compares the two values and returns the one that is larger.
            streak_id.last_completed = today
            streak_id.save()

        return redirect('show_streaks')


@login_required
def edit_streak(request, pk):
    today = timezone.localdate()
    streak = get_object_or_404(Streak, pk=pk, user=request.user)
    if request.method == 'POST':
        # Bind form to the POST data and the existing streak instance
        form = StreakForm(request.POST, instance=streak)
        if form.is_valid():
            streak.updated_at = today
            form.save()# Updates title/description
            messages.success(request, 'Streak updated.')
            return redirect('show_streaks')
        
    else:
    # Instantiate form with the existing streak data
        form = StreakForm(instance=streak)

    return render(request, 'streaks/edit_streak.html', {'form': form, 'streak': streak})


@login_required
def delete_streak(request, pk):
    today = timezone.localdate()
    streak = get_object_or_404(Streak, pk=pk, user=request.user)
    if request.method == 'POST':
        streak.is_active=False
        streak.is_deleted=True
        streak.deleted_at=today
        streak.save()
        messages.info(request, f'deleted streak {streak.title}')
        return redirect('show_streaks')
    
    return redirect('show_streaks')

