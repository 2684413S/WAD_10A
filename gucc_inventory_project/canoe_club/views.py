from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from canoe_club.models import Trip, Social, Kit, UserProfile, User
import datetime
from .forms import UserForm, UserProfileForm, UserUpdateForm, PasswordUpdateForm, PasswordResetForm, KitForm
from .decorators import user_not_authenticated
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str

def index(request):
    today = datetime.datetime.today()
    trips_list = Trip.objects.filter(date__gte=today).order_by("date")[:5]
    social_list = Social.objects.filter(date__gte=today).order_by("date")[:5]

    # print(social_list)
    context_dixt = {}
    context_dixt["trips"] = trips_list
    context_dixt["socials"] = social_list
    return render(request, 'canoe_club/index.html', context_dixt)

# Create your views here.

def about(request):
    return render(request, 'canoe_club/about.html')


def main_shed(request):
    wetsuit = Kit()
    wetsuit.amount = 30
    print(request.method)
    if request.method == 'POST':
        change = request.POST['change']
        print(change)
        if change == '-1':
            print('test')
            wetsuit.amount -= 1
            print(wetsuit.amount)
        elif change == '1':
            print('test+')
            wetsuit.amount += 1
            print(wetsuit.amount)
        elif change == 'move':
            print('mooove')
            # move_kit(request)
        elif change == 'remove':
            print('remo#ove')
            # remove_kit(request)

    return render(request, 'canoe_club/main_shed.html', {'kit_list': [wetsuit]})

def add_kit(request):
    form = KitForm()

    if request.method == "POST":
        form = KitForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request, 'canoe_club/add_kit.html')
        else:
            print(forms.errors)
    return render(request, 'canoe_club/add_kit.html', {'form':form})

def remove_kit(request):
    return render(request, 'canoe_club/remove_kit.html')

def move_shed(request):
    return render(request, 'canoe_club/move_shed.html')


def maintenance_shed(request):
    wetsuit = Kit()
    wetsuit.amount = 30
    print(request.method)
    if request.method == 'POST':
        change = request.POST['change']
        print(change)
        if change == '-1':
            print('test')
            wetsuit.amount -= 1
            print(wetsuit.amount)
        elif change == '1':
            print('test+')
            wetsuit.amount += 1
            print(wetsuit.amount)
        elif change == 'move':
            print('mooove')
            # move_kit(request)
        elif change == 'remove':
            print('remo#ove')
            # remove_kit(request)

    return render(request, 'canoe_club/maintenance_shed.html', {'kit_list': [wetsuit]})

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

def user_profile(request,username):
    try:
        selected_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect(reverse('canoe_club:index'))

    profile = UserProfile.objects.get(user=selected_user)

    return render(request,"canoe_club/profile.html",{"selected_user":selected_user,"profile":profile})

@login_required
def change_password(request):
    print("password")
    passsword_changed = False
    if request.method == "POST":
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            passsword_changed = True
        else:
            print(form.errors)
    else:
        form = PasswordUpdateForm(request.user)
    return render(request, 'accounts/change_password.html', {"form":form, "password_changed":passsword_changed})

@user_not_authenticated
def reset_password(request):
    email_sent = False
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data["email"]
            user_data = User.objects.get(email__exact=user_email)
            if user_data:
                subject = "Password Reset Request"
                message = render_to_string("password_reset_templates/password_reset_template.html", {
                    "user": user_data,
                    "domain": get_current_site(request).domain,
                    "user_id": urlsafe_base64_encode(force_bytes(user_data.username)),
                    "protocol": "https" if request.is_secure() else "http"
                })

                email = EmailMessage(subject,message, to=[user_email])
                if email.send():
                    email_sent = True
                else:
                    print("Problem sending email...")
            else:
                return redirect(reverse("canoe_club:index"))
    else:
        form = PasswordResetForm()

    return render(request, "accounts/reset_password.html", {"form":form, "email_sent":email_sent})
def password_reset_confirm(request, uidb64):
    password_changed = False
    username = force_str(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("Link invalid" + username)
    if user:
        if request.method == 'POST':
            form = PasswordUpdateForm(user, request.POST)
            if form.is_valid():
                form.save()
                password_changed = True
            else:
                print(form.errors)
        else:
            form = PasswordUpdateForm(user)
        return render(request, 'password_reset_templates/password_reset_confirm.html', {'form': form,"password_changed":password_changed})
    else:
        return HttpResponse("Link has expired")

def edit_profile(request):
    # user_form = UserUpdateForm(request.POST, instance = request.user)
    # profile_form = UserProfile(request.POST, instance = request.user)
    return render(request, 'accounts/edit_profile.html')

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
            login(request,user)
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {}
    context_dict["user_form"] = user_form
    context_dict["profile_form"] = profile_form
    context_dict["registered"] = registered
    return render(request, "accounts/register.html", context_dict)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse("canoe_club:index"))
            else:
                return HttpResponse("Your canoe club account has been deactivated")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    return render(request, "accounts/login.html")

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect(reverse("canoe_club:index"))

    return render(request, "accounts/logout.html")

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
