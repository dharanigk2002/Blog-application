from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Get all employees"
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM blog_post")
            rows = cursor.fetchall()
        for row in rows:
            print(row)
        self.stdout.write(self.style.SUCCESS("Successfully fetched"))