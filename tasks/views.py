from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task, Profile
from .serializers import TaskSerializer

import random


# ================= HOME PAGE =================
def home(request):

    if not request.user.is_authenticated:
        return redirect('login')

    total_tasks = Task.objects.filter(
        user=request.user
    ).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        status='Completed'
    ).count()

    pending_tasks = Task.objects.filter(
        user=request.user,
        status='Pending'
    ).count()

    recent_tasks = Task.objects.filter(
        user=request.user
    ).order_by('-id')

    context = {

        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'recent_tasks': recent_tasks,

    }

    return render(
        request,
        'home.html',
        context
    )


# ================= LOGIN =================
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'login.html'
    )


# ================= REGISTER =================
def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists'
            )

            return redirect('register')

        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Email already exists'
            )

            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        Profile.objects.create(user=user)

        messages.success(
            request,
            'Account created successfully'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# ================= LOGOUT =================
def logout_view(request):

    logout(request)

    return redirect('login')


# ================= ADD TASK =================
def add_task(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        title = request.POST.get('title')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')
        status_value = request.POST.get('status')

        if not status_value:
            status_value = 'Pending'

        Task.objects.create(

            user=request.user,
            title=title,
            priority=priority,
            deadline=deadline,
            status=status_value

        )

        messages.success(
            request,
            'Task added successfully'
        )

        return redirect('home')

    return render(
        request,
        'add_task.html'
    )


# ================= UPDATE TASK =================
def update_task(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority')
        task.deadline = request.POST.get('deadline')
        task.status = request.POST.get('status')

        task.save()

        messages.success(
            request,
            'Task updated successfully'
        )

        return redirect('home')

    return render(
        request,
        'update_task.html',
        {'task': task}
    )


# ================= DELETE TASK =================
def delete_task(request, id):

    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    task.delete()

    messages.success(
        request,
        'Task deleted successfully'
    )

    return redirect('home')


# ================= COMPLETED TASKS =================
def completed_tasks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.filter(

        user=request.user,
        status='Completed'

    ).order_by('-id')

    return render(
        request,
        'completed_tasks.html',
        {'tasks': tasks}
    )


# ================= PENDING TASKS =================
def pending_tasks(request):

    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.filter(

        user=request.user,
        status='Pending'

    ).order_by('-id')

    return render(
        request,
        'pending_tasks.html',
        {'tasks': tasks}
    )


# ================= FORGOT PASSWORD =================
def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        try:

            user = User.objects.get(email=email)

            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            try:

                send_mail(

                    'Password Reset OTP',

                    f'Your OTP is: {otp}',

                    settings.EMAIL_HOST_USER,

                    [email],

                    fail_silently=False,

                )

                messages.success(
                    request,
                    'OTP sent successfully to your email'
                )

                return redirect('verify_otp')

            except Exception as e:

                print("EMAIL ERROR:", e)

                messages.error(
                    request,
                    f'Email sending failed: {e}'
                )

        except User.DoesNotExist:

            messages.error(
                request,
                'Email does not exist'
            )

    return render(
        request,
        'forgot_password.html'
    )


# ================= VERIFY OTP =================
def verify_otp(request):

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        saved_otp = request.session.get('reset_otp')

        if entered_otp == saved_otp:

            return redirect('reset_password')

        else:

            messages.error(
                request,
                'Invalid OTP'
            )

    return render(
        request,
        'verify_otp.html'
    )


# ================= RESET PASSWORD =================
def reset_password(request):

    if request.method == 'POST':

        password = request.POST.get('password')

        email = request.session.get('reset_email')

        if email:

            user = User.objects.get(email=email)

            user.set_password(password)

            user.save()

            request.session.flush()

            messages.success(
                request,
                'Password reset successful'
            )

            return redirect('login')

    return render(
        request,
        'reset_password.html'
    )


# ==================================================
# ===================== APIs =======================
# ==================================================


# ================= GET ALL TASKS =================
@api_view(['GET'])
def api_task_list(request):

    tasks = Task.objects.all()

    serializer = TaskSerializer(
        tasks,
        many=True
    )

    return Response(serializer.data)


# ================= GET SINGLE TASK =================
@api_view(['GET'])
def api_task_detail(request, pk):

    try:

        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(task)

    return Response(serializer.data)


# ================= CREATE TASK API =================
@api_view(['POST'])
def api_create_task(request):

    serializer = TaskSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# ================= UPDATE TASK API =================
@api_view(['PUT'])
def api_update_task(request, pk):

    try:

        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(
        task,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# ================= DELETE TASK API =================
@api_view(['DELETE'])
def api_delete_task(request, pk):

    try:

        task = Task.objects.get(id=pk)

    except Task.DoesNotExist:

        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    task.delete()

    return Response(
        {'message': 'Task deleted successfully'},
        status=status.HTTP_204_NO_CONTENT
    )