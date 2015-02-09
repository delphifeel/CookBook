from setuptools.compat import unicode
from recipes.management.commands.parser import IParser
from recipes.models import Recipe, Ingredient, RecipeIngredients, Unit
import re
import urllib.request
import time


def get_frac(data):
    if '&frac' in data:
        reg = re.compile(r'.*(&.*;).*')
        reg = reg.search(data)
        s = reg.group(1)
        s = s[5:]
        s = s.replace(';', '')
        n = s[0]
        d = s[1]
        return float(int(n) / int(d))

def remove_frac(data):
    result = data
    if '&frac' in data:
        reg = re.compile(r'.*(&.*;).*')
        it = reg.findall(data)
        for s in it:
            result = result.replace(s, '')
    return result


def to_str(data):
    result = data
    # remove &nbsp;
    result = result.replace('&nbsp;', ' ')

    # remove all &.*; elements
    reg = re.compile(r'.*(&.*;).*')
    it = reg.findall(result)
    for s in it:
        result = result.replace(s, '')

    result = result.strip()
    return result


class EdaRuParser(IParser):
    def url(self):
        return 'eda.ru'

    def execute(self):
        reg = re.compile(r'<a id="link-recipewidget-recipeName-\d+" href="(http://eda.ru/salad/recipe.*?)">(.*?)</a>')
        reg_ingredient_name = re.compile(r'<td class="name"><span>(.*?)</span></td>|'
                                         r'<a id="link-recipe-ingredientPreview.*?".*?>(.*?)</a>')
        reg_ingredient_amount = re.compile(r'<span class="amount">([0-9]*,?[0-9]*)(.*?)</span>')

        for i in range(1, 2):
            print('Parsing page number {}'.format(i))

            data = urllib.request.urlopen('http://eda.ru/recipelist/salad/page{}'.format(i)).read()
            data = data.decode('utf8')

            data_all = reg.findall(data)
            for (recipe_url, recipe_name) in data_all:
                recipe_name = to_str(recipe_name)
                rec_list = Recipe.objects.filter(name=recipe_name)
                if len(rec_list) == 0:
                    rec = Recipe()
                    rec.name = recipe_name
                    rec.url = recipe_url
                    rec.save()
                else:
                    continue

                ingredients = []

                data = urllib.request.urlopen(recipe_url).read()
                data = data.decode('utf8')

                data_all = reg_ingredient_name.findall(data)
                for ing_name1, ing_name2 in data_all:
                    ing_name = ing_name1 if ing_name1 != '' else ing_name2
                    ing_name = to_str(ing_name)
                    got, created = Ingredient.objects.get_or_create(name=ing_name)
                    ing = got if got else created
                    ingredients.append(ing)

                data_all = reg_ingredient_amount.findall(data)
                k = 0
                for ing_amount, ing_unit in data_all:
                    ing_unit = to_str(ing_unit)
                    ri = RecipeIngredients()
                    ri.recipe = rec
                    ri.ingredient = ingredients[k]

                    fr = get_frac(ing_unit)
                    if fr:
                        ing_amount = fr
                        ing_unit = remove_frac(ing_unit)
                    else:
                        ing_amount = ing_amount.replace(',', '.')
                        ing_amount = ing_amount if ing_amount != '' else 0

                    ri.amount = ing_amount
                    got, created = Unit.objects.get_or_create(name=ing_unit)
                    unit = got if got else created
                    ri.unit = unit
                    ri.save()

                    k += 1