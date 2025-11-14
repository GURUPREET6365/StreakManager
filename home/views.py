from django.shortcuts import render, get_object_or_404, redirect
# Here i am importing the Streak table from streaks app model file
from streaks.models import Streak
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from daily_goals.models import UsersGoals
from .models import ultimateGoal
from django.contrib import messages
from datetime import timedelta
from .forms import UltimateGoalForm

# Create your views here.
def home(request):
    #  it creates a queryset limited to rows where the Streak.user foreign key equals the current request.user only.  It is equivalent to “SELECT … FROM streaks WHERE user_id = current_user_id”
    # streaks = Streak.objects.filter(user=request.user) request.user represents an AnonymousUser object. This object does not have a primary key (pk) or id attribute, as it doesn't correspond to a specific user in the database.
    ultimate_goal = ultimateGoal.objects.filter(user_id=request.user.id)
    ult_goal_list = []
    for ult_goal in ultimate_goal:
        ult_goal_list.append(ult_goal)


    today = timezone.localdate() 
    incomplete_goal = []
        # below are the two boolean checkng statement that check and return true or false.
    goals = UsersGoals.objects.filter(user_id=request.user.id, is_deleted = False, is_active=True)
    for i_goal in goals:
        created_date = timezone.localdate(i_goal.created_at)
        deadline_date = created_date + timedelta(days=1)
        if not i_goal.completed and (today <= deadline_date):  # Checks if the goal is not completed (i.e., goal.completed is False)
            incomplete_goal.append(i_goal) 


    incomplete_streaks = []
    streaks = Streak.objects.filter(user_id=request.user.id, is_deleted = False, is_active=True)
    for i_streaks in streaks:
        if i_streaks.last_completed != today:
            incomplete_streaks.append(i_streaks)
            
    return render(request, 'home/home.html', {'streaks':streaks, 'incomplete_streaks':incomplete_streaks, 'incomplete_goal':incomplete_goal, 'goals':goals, 'ult_goal_list':ult_goal_list, 'ultimate_goal':ultimate_goal})


def about_us(request):
    return render(request, 'home/about_us.html')

@login_required
def ultimategoal(request):
    updated_date = timezone.now()
    if request.method == 'POST':
        title = request.POST.get('title')
        
        ultgoal, created = ultimateGoal.objects.update_or_create(
            user=request.user,
            defaults={'title': title, 'updated_at': updated_date}
        )
        if created:
            messages.success(request, 'The ultimate goal has been created.')
        else:
            messages.success(request, 'Your ultimate goal has been updated.')
       
        return redirect('home')
      # For a GET request, we still need to retrieve the existing goal
    # to display it in the template.
    try:
        existing_goal = ultimateGoal.objects.get(user=request.user)
    except ultimateGoal.DoesNotExist:
        existing_goal = None
    
    context = {
        'existing_goal': existing_goal
    }
    return render(request, 'home/ultimategoal.html', context)


@login_required
def edit_ultimate_goal(request):
    goal = ultimateGoal.objects.get(user=request.user)  # 👈 fetch via OneToOne

    if request.method == 'POST':
        form = UltimateGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your Ultimate Goal has been saved successfully')
            return redirect('home')
          # redirect wherever needed
    else:
        form = UltimateGoalForm(instance=goal)  # 👈 prefill form

    return render(request, 'home/editultimategoal.html', {'form': form})


def deleteultimategoal(request):
    goal = ultimateGoal.objects.get(user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.info(request,'Goal has been deleted.')
        return redirect('home')
    
    return redirect('home')