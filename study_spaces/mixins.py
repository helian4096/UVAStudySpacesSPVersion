"""
 REFERENCES

 Title: did_django_google_maps_api
 Author: Bobby Stearman
 Date: 04/16/2021
 Code version: N/A
 URL: https://www.youtube.com/watch?v=wCn8WND-JpU
 Software License: GPL-3.0 license
 """

from django.conf import settings
import requests
import json

def Directions(*args, **kwargs):
    lat_a = kwargs.get("lat_a")
    long_a = kwargs.get("long_a")
    lat_b = kwargs.get("lat_b")
    long_b = kwargs.get("long_b")

    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'

    result = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?',
        params={
            'origin': origin,
            'destination': destination,
            "key": settings.GOOGLE_API_KEY,
            'mode': 'walking'
        })

    directions = result.json()

    if directions["status"] == "OK":
        route = directions["routes"][0]["legs"][0]
        origin = route["start_address"]
        destination = route["end_address"]
        distance = route["distance"]["text"]
        duration = route["duration"]["text"]

        steps = [
            [
                s["distance"]["text"],
                s["duration"]["text"],
                s["html_instructions"],

            ]
            for s in route["steps"]]

    return {
        "origin": origin,
        "destination": destination,
        "distance": distance,
        "duration": duration,
        "steps": steps
    }
