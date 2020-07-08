from django.shortcuts import render
from django.http import HttpResponse

from listings.models import Listing
from listings.models import Developer
from listings.choices import price_choices, bedroom_choices, neighborhood_choices


def index(request):
    listings = Listing.objects.order_by(
        '-list_date').filter(is_published=True)[:4]

    context = {
        'listings': listings,
        'neighborhood_choices': neighborhood_choices
    }

    return render(request, 'pages/index.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)