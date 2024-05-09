from django.shortcuts import render
from market.models import Stock

# Create your views here.
def stock(request):
    all_item_stock = Stock.objects.all()
    print(all_item_stock)
    context = {"all_item_stock": all_item_stock}
    return render(request, 'administrate/stock.html', context)
