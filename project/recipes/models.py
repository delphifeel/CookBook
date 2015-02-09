from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=80)


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')


class Unit(models.Model):
    name = models.CharField(max_length=20)


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.ForeignKey(Unit)

