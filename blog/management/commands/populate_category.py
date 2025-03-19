from django.core.management.base import BaseCommand
from blog.models import Category

class Command(BaseCommand):
    help = "It is used to populate categories"

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        categories = ["Science", "Technology", "Food", "Arts", "Sports"]
        for category_name in categories:
            Category.objects.create(name = category_name)
        self.stdout.write(self.style.SUCCESS("INSERTED CATEGORIES"))