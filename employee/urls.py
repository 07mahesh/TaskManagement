from django.urls import path
from employee import views

urlpatterns = [
    path('home/', views.home,name='home'),
    path('',views.login_page,name='login_page'),
    path('logout_page/',views.logout_page,name='logout_page'),
    path('register/',views.register,name='register'),
    path('policy/',views.policy,name='policy'),
    path('task/',views.task,name='task'),
    path('userpage/',views.userpage,name='userpage'),
    path('dashbord/',views.dashbord_view,name='dashbord'),
    path('calender/',views.task_calendar_data,name='calender'),
    path('calendar/data/', views.task_calendar_view, name='task_calendar_view'),
    path('user_profile/',views.user_profile_view,name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('chat/<str:room_name>/',views.chat_room, name='chat')


]
