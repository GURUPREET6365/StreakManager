from django.shortcuts import render, get_object_or_404, redirect
# Here i am importing the Streak table from streaks app model file

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from datetime import timedelta


# Create your views here.
def home(request):
    #  it creates a queryset limited to rows where the Streak.user foreign key equals the current request.user only.  It is equivalent to “SELECT … FROM streaks WHERE user_id = current_user_id”
    # streaks = Streak.objects.filter(user=request.user) request.user represents an AnonymousUser object. This object does not have a primary key (pk) or id attribute, as it doesn't correspond to a specific user in the database.


    today = timezone.localdate() 
    incomplete_goal = []
        # below are the two boolean checkng statement that check and return true or false.
    # goals = UsersGoals.objects.filter(user_id=request.user.id, is_deleted = False, is_active=True)
    # for i_goal in goals:
    #     created_date = timezone.localdate(i_goal.created_at)
    #     deadline_date = created_date + timedelta(days=1)
    #     if not i_goal.completed and (today <= deadline_date):  # Checks if the goal is not completed (i.e., goal.completed is False)
    #         incomplete_goal.append(i_goal) 


    # incomplete_streaks = []
    # streaks = Streak.objects.filter(user_id=request.user.id, is_deleted = False, is_active=True)
    # for i_streaks in streaks:
    #     if i_streaks.last_completed != today:
    #         incomplete_streaks.append(i_streaks)
            
    return render(request, 'home/home.html')


def about_us(request):
    return render(request, 'home/about_us.html')

