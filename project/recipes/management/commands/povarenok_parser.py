from setuptools.compat import unicode
from recipes.management.commands.parser import IParser
from recipes.models import Recipe, Ingredient, RecipeIngredients
import re
import urllib.request


class PovarenokParser(IParser):
    def url(self):
        return 'povarenok.ru'

    def execute(self):
        reg = re.compile(r'<a href="http://www.povarenok.ru/recipes/show/(\d+)/" title=".*?">(.*?)</a>')
        reg_ingredient_name = re.compile(r'<span itemprop="name">(.*?)</span>')
        reg_ingredient_amount = re.compile(r'<span itemprop="amount">(\d+)</span>')

        for i in range(1, 10):
            print('Parsing page number {}'.format(i))

            data = urllib.request.urlopen('http://www.povarenok.ru/recipes/~{}'.format(i)).read()
            data = data.decode('cp1251')
            data_all = reg.findall(data)
            for (code, recipe_name) in data_all:
                recipe_url = r'http://www.povarenok.ru/recipes/show/{}/'.format(code)
                rec = Recipe()
                rec.name = recipe_name
                rec.url = recipe_url
                rec.save()

                ingredients = []

                data = urllib.request.urlopen('http://www.povarenok.ru/recipes/show/{}/'.format(code)).read()
                data = data.decode('cp1251')

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



