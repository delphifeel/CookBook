from django.core.management import BaseCommand
from recipes.management.commands.eda_parser import EdaRuParser


class Worker:
    parsers = [EdaRuParser()]

    def parse(self, url):
        found = False
        for p in self.parsers:
            if p.url() == url:
                p.execute()
                found = True

        if not found:
            raise Exception('Parser {} not implemented'.format(url))


class Command(BaseCommand):
    def handle(self, *args, **options):
        w = Worker()
        w.parse('eda.ru')