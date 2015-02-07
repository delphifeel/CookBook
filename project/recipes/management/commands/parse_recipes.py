from django.core.management import BaseCommand
from recipes.management.commands.povarenok_parser import PovarenokParser
from recipes.models import Recipe, Ingredient, RecipeIngredients


class Command(BaseCommand):
    def handle(self, *args, **options):
        parser = PovarenokParser()
        parser.execute()