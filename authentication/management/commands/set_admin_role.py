from django.core.management.base import BaseCommand
from authentication.models import User

class Command(BaseCommand):
    help = 'Set a user as admin by email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to make admin')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        try:
            user = User.objects.get(email=email)
            user.role = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set {email} as admin'))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User with email {email} does not exist'))
