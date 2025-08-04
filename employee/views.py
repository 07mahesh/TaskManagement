from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . decorator import unauthenticated,adminonly
from django.contrib.auth.models import Group
from .models import Task,Department
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import UserProfile
from .models import Message
from django.db.models import Q
from datetime import datetime






@login_required(login_url='login_page')
def home(request):
    return render(request, 'home.html')




@unauthenticated
def register(request):
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            role = request.POST.get('role')
            uploaded_image = request.FILES.get('profile_image')

            if password1 != password2:
                return render(request, 'REG.html', {'error': 'Passwords do not match'})

            if User.objects.filter(username=username).exists():
               return render(request, 'REG.html', {'error': 'Username already exists'})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
                
            )

            if not role:
                return render(request, 'REG.html', {'error': 'Please select a valid role'})
            
    

            # Assign group dynamically
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            UserProfile.objects.create(
                user=user,
                role=role,
                profile_image=uploaded_image,
                                
            )
            # group = Group.objects.get(name='users')
            # user.groups.add(group) 
            login(request, user)
            return redirect('userpage')  
        return render(request, 'REG.HTML')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


@unauthenticated
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'log.html', {'error': 'Invalid username or password'})
    return render(request, 'log.html')


def logout_page(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login_page')
@adminonly
def task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        department_id = request.POST.get('department')
        assigned_to_id = request.POST.get('assigned_to')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        profile_img=request.POST.get('profile_img')


        department = Department.objects.get(id=department_id)
        assigned_to = User.objects.get(id=assigned_to_id)

        Task.objects.create(
            title=title,
            description=description,
            department=department,
            assigned_to=assigned_to,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            status=status,
            
        )
        return redirect('userpage')  

    context = {
        'departments': Department.objects.all(),
        'users': User.objects.all()
    }

    
    return render(request, 'create_task.html', context)




def policy(request):
    return render(request,'pol.html')



@login_required(login_url='login_page')

def userpage(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    user_profile = UserProfile.objects.filter(user=request.user).first()  # Safe lookup
    context = {
        'tasks': tasks,
        'user_profile': user_profile
    }
    return render(request, 'user.html', context)



from django.shortcuts import render
from .models import Task

def dashbord_view(request):
    user_tasks = Task.objects.filter(assigned_to=request.user)
    total_count = user_tasks.count()
    pending_count = user_tasks.filter(status='Pending').count()
    inprogress_count = user_tasks.filter(status='In Progress').count()  
    completed_count = user_tasks.filter(status='Completed').count()
    recent_completed = user_tasks.filter(status='Completed').order_by('-end_date').first()
    nearest_due = user_tasks.exclude(status='Completed').order_by('end_date').first()
    pending_tasks = user_tasks.filter(status='Pending')
    inprogress_tasks = user_tasks.filter(status='In Progress')
    completed_tasks = user_tasks.filter(status='Completed')
    recent_tasks = Task.objects.filter(assigned_to=request.user).order_by('-start_date')[:5]
    user_profile = UserProfile.objects.filter(user=request.user).first()
    room_name = request.user.username  

    context = {
        'pending_count': pending_count,
        'inprogress_count': inprogress_count,
        'completed_count': completed_count,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        'completed_tasks': completed_tasks,
        'total_count':total_count,
        'recent_completed':recent_completed,
        'nearest_due':nearest_due,
        'user_tasks':user_tasks,
        'recent_tasks': recent_tasks,
        'user_profile':user_profile,
        'room_name': room_name,


    }
    return render(request, 'dashbord.html', context)


def task_calendar_data(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': task.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            'color': '#f39c12' if task.status == 'Pending' else '#3498db' if task.status == 'In progress' else '#2ecc71',
        })

    return JsonResponse(events, safe=False)



def task_calendar_view(request):    
    return render(request, 'calender.html') 


@login_required
def user_profile_view(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
            profile.save()

        return redirect('user_profile')  # ✅ POST response

    # 🧾 This handles the GET request!
    return render(request, 'user_update_profile.html', {'profile': profile})


@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id) 
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # Sort user_last_messages by the timestamp of the last_message in descending order
        user_last_messages.sort(
            key=lambda x: x['last_message'].timestamp if x['last_message'] else datetime.min,
            reverse=True
        )


    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })


    # pending_count = user_tasks.filter(status='Pending').count()
    # inprogress_count = user_tasks.filter(status='In progress').count()
    # completed_count = user_tasks.filter(status='Completed').count()
    # pending_tasks = user_tasks.filter(status='Pending')
    # inprogress_tasks = user_tasks.filter(status='In progress')
    # completed_tasks= user_tasks.filter(status='Completed')

        #'pending_count': pending_count,
        # 'inprogress_count': inprogress_count,
        # 'completed_count': completed_count,
        # 'pending_tasks':pending_tasks,
        # 'inprogress_tasks':inprogress_tasks,
        # 'completed_tasks':completed_tasks


        