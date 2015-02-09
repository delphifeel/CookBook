import json
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


# Parse data like:
# [{"item": "Помидоры", "amount": "1.5"}]
# or
# [{"item": "Соль"}]
# or
# [{"item": "Соль", "amount": "100"}, {"item": "Помидоры"}]
from recipes.models import Ingredient, RecipeIngredients


@csrf_exempt
# TODO
def api(request):
    if request.method != 'POST':
        raise Http404

    body = request.body
    if not body:
        raise Http404

    body = body.decode('utf8')
    data = json.loads(body)
    q = Q()
    for obj in data:
        item_name = obj['item']
        if 'amount' in obj:
            item_amount = float(obj['amount'])
        else:
            item_amount = 0

        ing_list = Ingredient.objects.filter(name__contains=item_name)
        q_ing = Q()
        for ing in ing_list:
            q_ing |= Q(ingredient=ing)

        q_amount = Q()
        if item_amount != 0:
            q_amount = Q(amount__lte=item_amount)

        q &= ((q_ing) & q_amount)

    ri = RecipeIngredients.objects.filter(q)





    return HttpResponse('Hello world', content_type='application/json; charset=UTF-8')
