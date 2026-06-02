from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path(
        '',
        views.home,
        name='home'
    ),

    # LOGIN
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # REGISTER
    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # LOGOUT
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ADD TASK
    path(
        'add-task/',
        views.add_task,
        name='add_task'
    ),

    # UPDATE TASK
    path(
        'update-task/<int:id>/',
        views.update_task,
        name='update_task'
    ),

    # DELETE TASK
    path(
        'delete-task/<int:id>/',
        views.delete_task,
        name='delete_task'
    ),

    # COMPLETED TASKS
    path(
        'completed/',
        views.completed_tasks,
        name='completed_tasks'
    ),

    # PENDING TASKS
    path(
        'pending/',
        views.pending_tasks,
        name='pending_tasks'
    ),

    # FORGOT PASSWORD
    path(
        'forgot-password/',
        views.forgot_password,
        name='forgot_password'
    ),

    # VERIFY OTP
    path(
        'verify-otp/',
        views.verify_otp,
        name='verify_otp'
    ),

    # RESET PASSWORD
    path(
        'reset-password/',
        views.reset_password,
        name='reset_password'
    ),

    # ================= API URLs =================

    # GET ALL TASKS
    path(
        'api/tasks/',
        views.api_task_list,
        name='api_task_list'
    ),

    # GET SINGLE TASK
    path(
        'api/tasks/<int:pk>/',
        views.api_task_detail,
        name='api_task_detail'
    ),

    # CREATE TASK
    path(
        'api/tasks/create/',
        views.api_create_task,
        name='api_create_task'
    ),

    # UPDATE TASK
    path(
        'api/tasks/update/<int:pk>/',
        views.api_update_task,
        name='api_update_task'
    ),

    # DELETE TASK
    path(
        'api/tasks/delete/<int:pk>/',
        views.api_delete_task,
        name='api_delete_task'
    ),

]