from django.http import HttpResponse
from django.views.decorators.http import require_POST

from orders.forms import OrderCostForm
from orders.utils import get_order_cost


@require_POST
def calculate_order(request):
    form = OrderCostForm(request.POST)

    if not form.is_valid():
        return HttpResponse(request, {'form': form})

    order_cost = get_order_cost(request.POST)

    return HttpResponse(request, {'order_cost': order_cost})
