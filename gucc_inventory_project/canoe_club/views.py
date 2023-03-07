from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from canoe_club.models import Trip, Social, Kit
import datetime
from .forms import UserForm, UserProfileForm

def index(request):
    today = datetime.datetime.today()
    trips_list = Trip.objects.filter(date__gte=today).order_by("date")[:5]
    social_list = Social.objects.filter(date__gte=today).order_by("date")[:5]

    print(social_list)
    context_dixt = {}
    context_dixt["trips"] = trips_list
    context_dixt["socials"] = social_list
    return render(request, 'canoe_club/index.html', context_dixt)

# Create your views here.

def about(request):
    return render(request, 'canoe_club/about.html')


def main_shed(request):
    return render(request, 'canoe_club/main_shed.html')

def add_kit(request):
    return render(request, 'canoe_club/add_kit.html')

def remove_kit(request):
    return render(request, 'canoe_club/remove_kit.html')

def move_shed(request):
    return render(request, 'canoe_club/move_shed.html')


def maintenance_shed(request):
    return render(request, 'canoe_club/maintenance_shed.html')

def kit(request, kit_name_slug):

    try:
        kit = Kit.objects.get(slug = kit_name_slug)
        context_dict["kit"] = kit

    except Kit.DoesNotExist:
        context_dict["kit"] = None

    return render(request, "canoe_club/kit.html", context_dict)

def move_kit(request, kit_name_slug):
    return render(request, "canoe_club/move_kit.html")

def user_login(request):
    return render(request, 'canoe_club/login.html')

def profile(request):
    return render(request,"canoe_club/profile.html")

def change_password(request):
    return render(request, 'canoe_club/change_password.html')

def edit_profile(request):
    return render(request, 'canoe_club/edit_profile.html')

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {}
    context_dict["user_form"] = user_form
    context_dict["profile_form"] = profile_form
    context_dict["registered"] = registered
    return render(request, "canoe_club/register.html", context_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if user_is_active:
                login(request,user)
                return redirect(reverse("canoe_club:index"))
            else:
                return HttpResponse("Your canoe club account has been deactivated")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    return render(request, "canoe_club/login.html")

def socials(request):
    today = datetime.datetime.today()
    social_list = Social.objects.order_by("-date")
    context_dixt = {}
    context_dixt["socials"] = social_list
    return render(request, "canoe_club/socials.html", context_dixt)

def add_social(request):
    return render(request, "canoe_club/add_social.html")

def remove_social(request):
    return render(request, "canoe_club/remove_social.html")


def trips(request):
    today = datetime.datetime.today()
    trip_list = Trip.objects.order_by("-date")
    context_dixt = {}
    context_dixt["trips"] = trip_list
    return render(request, "canoe_club/trips.html", context_dixt)


def trip(request, trip_name_slug):

    try:
        trip = Trip.objects.get(slug = kit_name_slug)
        context_dict["trip"] = trip

    except Trip.DoesNotExist:
        context_dict["trip"] = None

    return render(request, "canoe_club/trip.html", context_dict)

def add_trip_member(request):
    return render(request, "canoe_club/trips/trip/member/add_member.html")

def remove_trip_member(request):
    return render(request, "canoe_club/trips/trip/member/remove_member.html")

def add_trip(request):
    return render(request, "canoe_club/trips/trip/add_trip.html")

def remove_trip(request):
    return render(request, "canoe_club/trips/trip/remove_trip.html")
