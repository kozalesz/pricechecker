from django.shortcuts import render
from django.views import View
from .models import Runcolors
from django.core.paginator import Paginator


class GlownaView(View):

    def get(self, request):
        search = request.GET.get('search', None)
        brand = request.GET.get('brand', None)
        page_id = request.GET.get('page', 1)
        if search:
            pagi = Paginator(Runcolors.objects.filter(product_number__icontains=search), 30)
        elif brand:
            pagi = Paginator(Runcolors.objects.filter(brand=brand), 30)
            brand = "&brand={}".format(brand)
        else:
            pagi = Paginator(Runcolors.objects.all(), 30)
            brand = ''
        if not pagi.count:
            komunikat = "Brak wyników!"
        else:
            komunikat = None
        ctx = {
            'paginator': pagi,
            'buty': pagi.page(page_id),
            'page': page_id,
            'brand': brand,
            'text': komunikat,
        }
        return render(request, 'glowna.html', ctx)

    def post(self, request):
        pagi = Paginator(Runcolors.objects.order_by('-steal'), 30)
        page_id = request.GET.get('page', 1)
        ctx = {
            'paginator': pagi,
            'buty': pagi.page(page_id),
            'page': page_id,
        }
        return render(request, 'glowna.html', ctx)


