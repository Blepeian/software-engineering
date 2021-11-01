#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.shortcuts import render
import requests


def board(request):
    data = requests.get("https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=3&sort=-departure_time&filter%5Bstop%5D=place-north").json()
    vehicles = []

    for i in range(0, 3):
        vehicle = []

        route_id = data["data"][i]["relationships"]["route"]["data"]["id"]
        direction = data["data"][i]["attributes"]["direction_id"]
        route = requests.get("https://api-v3.mbta.com/routes/" + route_id).json()

        vehicle.append(data["data"][i]["attributes"]["arrival_time"])
        vehicle.append(data["data"][i]["attributes"]["departure_time"])
        vehicle.append(route["data"]["attributes"]["direction_destinations"][direction])

        vehicles.append(vehicle)
    return render(request, "board.html", {"vehicles": vehicles})


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kalin.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
