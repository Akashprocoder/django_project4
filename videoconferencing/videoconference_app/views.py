from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')



class VideoConferenceView(View):
    def post(self, request):
        # Handle signaling messages from clients
        data = request.POST
        action = data.get('action')
        room_id = data.get('room_id')
        user_id = data.get('user_id')
        message = data.get('message')
        
        if action == 'join_room':
            # Handle joining a video conference room
            self.join_room(room_id, user_id)
        elif action == 'leave_room':
            # Handle leaving a video conference room
            self.leave_room(room_id, user_id)
        elif action == 'send_message':
            # Handle sending signaling messages to other participants
            self.send_message(room_id, user_id, message)
        
        return JsonResponse({'status': 'success'})

    def join_room(self, room_id, user_id):
        # Perform actions when a user joins a room
        pass

    def leave_room(self, room_id, user_id):
        # Perform actions when a user leaves a room
        pass

    def send_message(self, room_id, user_id, message):
        # Send signaling messages to other participants in the room
        pass

