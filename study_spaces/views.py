"""
 REFERENCES

 Title: did_django_google_maps_api
 Author: Bobby Stearman
 Date: 04/16/2021
 Code version: N/A
 URL: https://www.youtube.com/watch?v=wCn8WND-JpU
 Software License: GPL-3.0 license

 Title: Items in JSON object are out of order using "json.dumps"?
 Author: jfs
 Date: 12/20/2017
 Code version: N/A
 URL: https://stackoverflow.com/questions/10844064/items-in-json-object-are-out-of-order-using-json-dumps
 Software License: N/A
 
 Title: Lambda Sorted in Python - How to Lambda Sort a List
 Author: Kolade Chris
 Date: 03/16/2023
 Code version: N/A
 URL: https://www.freecodecamp.org/news/lambda-sort-list-in-python/
 Software License: N/A
 """


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from .mixins import Directions
import json

from .models import *


def is_admin(email):
    admins = [
        'lukecreech11@gmail.com',
        'rqf8pe@virginia.edu',
        'gracefly4@gmail.com',
        'ethanhaller02@gmail.com',
        'cs3240.super@gmail.com',
        'projecta06testuser@gmail.com'
    ]

    return email in admins


def get_approved_spaces():
    return StudySpace.objects.filter(approved_submission=StudySpace.ApprovalStatus.APPROVED)


def get_pending_spaces():
    return StudySpace.objects.filter(approved_submission=StudySpace.ApprovalStatus.PENDING)


def get_spaces_by_email(email):
    return StudySpace.objects.filter(user_email=email).order_by('-time_created')


@login_required(login_url='/study/login')
def home(request):
    mod = get_approved_spaces()
    mod_json = json.dumps(list(mod.values('latitude', 'longitude', 'id', 'name')))
    context = {
        'mod': mod,
        'mod_json': mod_json,
        'key': settings.GOOGLE_API_KEY,
    }
    return render(request, "study_spaces/studyspaces.html", context)


def logout_view(request):
    logout(request)
    return redirect("/study/")


@login_required(login_url='/study/login')
def directions(request):
    mod_json = []
    s = None
    if "dest" in request.GET:
        s = StudySpace.objects.get(pk=request.GET["dest"])
        s = {'latitude': s.latitude, 'longitude': s.longitude, 'id': s.id, 'name': s.name, 'address': s.address}
        mod_json = json.dumps(s)

    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")
    directions = None
    showDirections = False
    if lat_a and long_a and lat_b and long_b:
        directions = Directions(
            lat_a=lat_a,
            long_a=long_a,
            lat_b=lat_b,
            long_b=long_b,
        )
        showDirections = True
    context = {
        's': s,
        'mod_json': mod_json,
        'key': settings.GOOGLE_API_KEY,
        'directions': directions,
        'showDirections': showDirections,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}'
    }
    return render(request, 'study_spaces/directions.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/study")
    else:
        return render(request, "study_spaces/login.html")


@login_required(login_url='/study/login')
def admin_view(request):
    if is_admin(request.user.email):
        return render(request, "study_spaces/admin.html")
    else:
        return redirect('/study')


@login_required(login_url='/study/login')
def profile(request):
    return render(request, 'study_spaces/profile.html')


@login_required(login_url='/study/login')
def submission(request):
    context = {"google_api_key": settings.GOOGLE_API_KEY, "toasts": messages.get_messages(request)}

    if is_admin(request.user.email):
        context["pending_list"] = get_pending_spaces()
        context["pending_list_length"] = len(context["pending_list"])
        context["approved_list"] = get_approved_spaces()
        context["approved_list_length"] = len(context["approved_list"])
        return render(request, 'study_spaces/approval.html', context)
    else:
        context["submitted_list"] = get_spaces_by_email(request.user.email)
        if request.method == 'POST':
            if request.POST["name"] == '':
                context["error_message"] = "Please input a name."
                return render(request, 'study_spaces/submission.html', context)
            if request.POST["address"] == '' or request.POST["lat"] == '' or request.POST["long"] == '':
                context["error_message"] = "Please input a valid address."
                return render(request, 'study_spaces/submission.html', context)

            s = StudySpace(
                name=request.POST["name"],
                address=request.POST["address"],
                latitude=request.POST["lat"],
                longitude=request.POST["long"],
                user_email=request.user.email,
                has_wifi = 'has_wifi' in request.POST,
                has_outlets = 'has_outlets' in request.POST,
                has_printers = 'has_printers' in request.POST,
                has_whiteboards = 'has_whiteboards' in request.POST,
                is_quiet = 'is_quiet' in request.POST,
                is_outside = 'is_outside' in request.POST,
                has_food = 'has_food' in request.POST,
                location=request.POST["location"],
                environment=request.POST["environment"],
                traffic=request.POST["traffic"],
                hours=request.POST["hours"],
                other_information=request.POST["other_information"],
                denial_reason = 'None'
            )
            s.save()
            messages.success(request, f'Study Space "{s.name}" has been successfully submitted.')
        context["submitted_list"] = get_spaces_by_email(request.user.email)
        context["submitted_list_length"] = len(context["submitted_list"])
        return render(request, 'study_spaces/submission.html', context)


@login_required(login_url='/study/login')
def approve_submission(request):
    if request.method == 'POST':
        s = StudySpace.objects.get(pk=request.POST["id"])
        s.approved_submission = StudySpace.ApprovalStatus.APPROVED
        s.save()
        messages.success(request, f'Study Space "{s.name}" has been successfully approved.')
    return redirect('/study/submission')


@login_required(login_url='/study/login')
def deny_submission(request):
    if request.method == 'POST':
        s = StudySpace.objects.get(pk=request.POST["id"])
        s.approved_submission = StudySpace.ApprovalStatus.DENIED
        s.denial_reason = request.POST["Denial"]
        s.save()
        messages.success(request, f'Study Space "{s.name}" has been successfully denied.')
    return redirect('/study/submission')


@login_required(login_url='/study/login')
def edit_study_space(request, study_space_id):
    if is_admin(request.user.email):
        space = StudySpace.objects.get(pk=study_space_id)
        context = {"study_space": space, "google_api_key": settings.GOOGLE_API_KEY}

        if request.method == 'POST':
            if request.POST["name"] == '':
                context["error_message"] = "Please input a name."
                return render(request, 'study_spaces/edit.html', context)
            if request.POST["address"] == '' or request.POST["lat"] == '' or request.POST["long"] == '':
                context["error_message"] = "Please input a valid address."
                return render(request, 'study_spaces/edit.html', context)

            space.name=request.POST["name"]
            space.address=request.POST["address"]
            space.latitude=request.POST["lat"]
            space.longitude=request.POST["long"]
            space.has_wifi= 'has_wifi' in request.POST
            space.has_outlets = 'has_outlets' in request.POST
            space.has_printers = 'has_printers' in request.POST
            space.has_whiteboards = 'has_whiteboards' in request.POST
            space.is_quiet = 'is_quiet' in request.POST
            space.is_outside = 'is_outside' in request.POST
            space.has_food = 'has_food' in request.POST
            space.location = request.POST["location"]
            space.environment = request.POST["environment"]
            space.traffic = request.POST["traffic"]
            space.hours = request.POST["hours"]
            space.other_information=request.POST["other_information"]
            space.approved_submission = StudySpace.ApprovalStatus.APPROVED
            space.denial_reason = 'None'
            space.save()
            messages.success(request, f'Saved changed to Study Space "{space.name}".')
            return redirect('/study/submission')
        return render(request, 'study_spaces/edit.html', context)
    return redirect('/study')


@login_required(login_url='/study/login')
def delete_study_space(request, study_space_id):
    if request.method == 'POST':
        try:
            space_to_delete = StudySpace.objects.get(pk=study_space_id)
            space_to_delete.delete()
            messages.success(request, f'Study Space "{space_to_delete.name}" has been successfully deleted.')
        except StudySpace.DoesNotExist:
            messages.error(request, 'Study Space does not exist.')

    return redirect('/study/submission')


@login_required(login_url='/study/login')
def information(request):
    context = {}
    if "dest" in request.GET:
        s = StudySpace.objects.get(pk=request.GET["dest"])
        context["study_space"] = s
    return render(request, 'study_spaces/information.html', context)


@login_required(login_url='/study/login')
def closest(request):
    mod = get_approved_spaces()
    context = {
        'mod': mod,
        'key': settings.GOOGLE_API_KEY,
    }
    if request.method == 'POST':
        if request.POST["address"] == '' or request.POST["lat"] == '' or request.POST["long"] == '':
            context["error_message"] = "Please input a valid address."
            return render(request, 'study_spaces/closest.html', context)
        input_lat = float(request.POST["lat"])
        input_long = float(request.POST["long"])
        spaces_list = list(mod.values('latitude', 'longitude', 'id', 'name', 'address'))
        sorted_spaces_list = (
            sorted(spaces_list,
                   key=lambda space:
                   (space['latitude'] - input_lat) ** 2 + (space['longitude'] - input_long) ** 2
                   ))
        mod = sorted_spaces_list
        context['mod'] = mod
        context['start_address'] = request.POST["address"]
    return render(request, 'study_spaces/closest.html', context)
