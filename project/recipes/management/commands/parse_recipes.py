from django.core.management import BaseCommand
from recipes.management.commands.eda_parser import EdaRuParser
from recipes.management.commands.povarenok_parser import PovarenokParser
from recipes.management.commands.test import TestParser
from recipes.models import Recipe, Ingredient, RecipeIngredients


class Command(BaseCommand):
    def handle(self, *args, **options):
        parser = TestParser()
        parser.execute()