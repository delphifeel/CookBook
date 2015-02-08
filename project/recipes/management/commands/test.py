from recipes.management.commands.parser import IParser
from recipes.models import Recipe


class TestParser(IParser):
    def url(self):
        return 'eda.ru'

    def execute(self):
        rec = Recipe()
        rec.name = 'Тест'
        rec.url = 'Test'
        rec.save()