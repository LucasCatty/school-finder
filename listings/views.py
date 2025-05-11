from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.views.generic import (ListView, DetailView)
from django.db.models import Q
from decimal import Decimal
from django.utils.html import format_html

from .models import Listing, ListingType
from core.models import State


class ListingListView(ListView):
    model = Listing
    template_name = 'listings/listings.html'
    paginate_by = 4
    object_list = Listing.objects.order_by('-created').filter(
        is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listings'] = self.object_list  # TODO change this bullshit
        # Showcase Section Infos
        context['title'] = _("Browse our properties")
        # SEO
        context['page_title'] = _("Browse Property Listings")
        context['page_description'] = _("Real estate manager."
                                        "Browse all properties we are "
                                        "offering.")
        return context


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['subtitle'] = format_html(f'<i class="fas fa-map-marker"></i>'
                                          f' {self.object.address}')
        # SEO
        context['page_title'] = self.object.title
        context['page_description'] = _("Real estate manager."
                                        "Description and attribute listing of "
                                        "a specific object you are "
                                        "interested in.")
        return context


def search(request):
    res = Listing.objects.order_by('-created')

    # existing filter parameters
    keywords = request.GET.get('keywords', "")
    city = request.GET.get('city', "")
    state = request.GET.get('state', "")
    listing_type = request.GET.get('listing_type', 0)
    min_sqft = request.GET.get('sqft', 0)
    max_price = request.GET.get('price', Decimal(10000000))
    # REMOVE min_bedrooms and min_bathrooms filters
    # Instead, add school_content filter
    school_content = request.GET.get('school_content', "").strip()

    # existing default value settings
    if not min_sqft:
        min_sqft = 0
    if not max_price:
        max_price = 1000000000

    # Start filtering
    queryset_list = res.filter(
        (Q(description__icontains=keywords) |
         Q(title__icontains=keywords)),
        address__city__icontains=city,
        sqft__gte=min_sqft,
        price__lte=max_price,
    )

    # existing filters for listing_type and state
    try:
        if isinstance(int(listing_type), int):
            queryset_list = queryset_list.filter(listing_type=listing_type)
    except Exception:
        pass

    try:
        if isinstance(int(state), int):
            queryset_list = queryset_list.filter(address__state=state)
    except Exception:
        pass

    # **Add filtering for "school content"**
    if school_content:
        # Filter listings where title or description contains the school content keyword
        queryset_list = queryset_list.filter(
            Q(description__icontains=school_content) |
            Q(title__icontains=school_content)
        )

    # prepare context
    context = {
        'states': State.objects.all(),
        'list_types': ListingType.objects.all(),
        'listings': queryset_list,
        'values': request.GET,
        # pass the current search value back to the template for the input
        'school_content': school_content,
    }

    return render(request, 'listings/_partials/_search.html', context)