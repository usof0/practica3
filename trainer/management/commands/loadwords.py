import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from trainer.models import Word

class Command(BaseCommand):
    help = 'Load words from CSV file or predefined list for a specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            help='Username to add words for'
        )
        parser.add_argument(
            '--userid',
            type=int,
            help='User ID to add words for'
        )
        parser.add_argument(
            '--csv',
            help='Path to CSV file containing words'
        )
        parser.add_argument(
            '--sample',
            action='store_true',
            help='Load sample words'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        try:
            # Get user
            user = self.get_user(options)
            if not user:
                self.list_users()
                return

            # Get words data
            words_data = self.get_words_data(options)
            if not words_data:
                raise CommandError("No words data provided")

            # Add words
            added_count = self.add_words_for_user(user, words_data)

            self.stdout.write(self.style.SUCCESS(
                f'\nSuccessfully added {added_count} words for {user.username}\n'
                f'Total words for user: {Word.objects.filter(user=user).count()}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

    def get_user(self, options):
        """Get user by username or ID"""
        User = get_user_model()
        if options['username']:
            return User.objects.get(username=options['username'])
        elif options['userid']:
            return User.objects.get(id=options['userid'])
        return None

    def list_users(self):
        """Display all available users"""
        User = get_user_model()
        self.stdout.write("\nAvailable users:")
        for user in User.objects.all().order_by('id'):
            self.stdout.write(f"ID: {user.id} | Username: {user.username}")

    def get_words_data(self, options):
        """Get words data from CSV or sample"""
        if options['csv']:
            return self.read_csv_file(options['csv'])
        elif options['sample']:
            return self.get_sample_words()
        return None

    def read_csv_file(self, file_path):
        """Read words from CSV file"""
        if not os.path.exists(file_path):
            raise CommandError(f"File not found: {file_path}")

        words = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                words.append({
                    'english': row.get('english', '').strip(),
                    'translation': row.get('translation', '').strip(),
                    'example': row.get('example', '').strip()
                })
        return words

    def get_sample_words(self):
        """Return sample words"""
        return [
            {'english': 'apple', 'translation': 'manzana', 'example': 'I eat an apple every morning.'},
            {'english': 'book', 'translation': 'libro', 'example': 'This book is very interesting.'},
            {'english': 'computer', 'translation': 'computadora', 'example': 'I work on my computer all day.'},
        ]

    def add_words_for_user(self, user, words_data):
        """Add words to database for specific user"""
        added_count = 0
        for word_data in words_data:
            if not word_data['english'] or not word_data['translation']:
                continue

            _, created = Word.objects.get_or_create(
                user=user,
                english=word_data['english'],
                defaults={
                    'translation': word_data['translation'],
                    'example': word_data.get('example', ''),
                    'is_learned': False
                }
            )
            if created:
                added_count += 1
        return added_count