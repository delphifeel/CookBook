from setuptools.compat import unicode
from recipes.management.commands.parser import IParser
from recipes.models import Recipe, Ingredient, RecipeIngredients
import re
import urllib.request
import time


class EdaRuParser(IParser):
    def url(self):
        return 'eda.ru'

    def execute(self):
        reg = re.compile(r'<a id="link-recipewidget-recipeName-\d+" href="(http://eda.ru/salad/recipe.*?)">(.*?)</a>')
        reg_ingredient_name = re.compile(r'<td class="name"><span>(.*?)</span></td>')
        reg_ingredient_amount = re.compile(r'<span class="amount">(\d+)</span>')

        for i in range(1, 2):
            print('Parsing page number {}'.format(i))

            data = urllib.request.urlopen('http://eda.ru/recipelist/salad/page{}'.format(i)).read()
            data = data.decode('utf8')
            #time.sleep(1)

            data_all = reg.findall(data)
            for (recipe_url, recipe_name) in data_all:
                rec = Recipe()
                rec.name = 'Привет тест'
                rec.url = recipe_url
                rec.save()

                ingredients = []

                data = urllib.request.urlopen(recipe_url).read()
                data = data.decode('utf8')
                #time.sleep(1)

                data_all = reg_ingredient_name.findall(data)
                for ing_name in data_all:
                    ing = Ingredient()
                    ing.name = ing_name
                    ing.save()
                    ingredients.append(ing)

                data_all = reg_ingredient_amount.findall(data)
                k = 0
                for ing_amount in data_all:
                    ri = RecipeIngredients()
                    ri.recipe = rec
                    ri.ingredient = ingredients[k]
                    ri.amount = ing_amount
                    ri.save()

                    k += 1



