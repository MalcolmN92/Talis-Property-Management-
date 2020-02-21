from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, neighborhood_choices
from django.template.loader import render_to_string

from .models import Listing


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/search.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    is_favorite = False

    if listing.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    context = {
        'listing': listing,
        'is_favorite': is_favorite
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    if 'neighborhood' in request.GET:
        neighborhood = request.GET['neighborhood']
        if neighborhood:
            queryset_list = queryset_list.filter(
                neighborhood__iexact=neighborhood)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'neighborhood_choices': neighborhood_choices,
        'listings': queryset_list,
        'values': request.GET,
        'listings': paged_listings
    }

    return render(request, 'listings/search.html', context)


def favorite_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.favorite.filter(id=request.user.id).exists():
        listing.favorite.remove(request.user)
    else:
        listing.favorite.add(request.user)
    return HttpResponseRedirect(listing.get_absolute_url())
