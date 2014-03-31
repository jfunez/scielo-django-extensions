from django.conf import settings
from django.core.management import call_command

def main():
    # the minimum necessary to get Django running
    settings.configure(
        INSTALLED_APPS=(
            'scielo_extensions',
            'django_coverage',
        ),
        DATABASE_ENGINE='sqlite3'
    )
    settings.PAGINATION__ITEMS_PER_PAGE = 5
    settings.DOCUMENTATION_BASE_URL = ''
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'scielo_extensions.db',         # Or path to database file if using sqlite3.
            'USER': '',               # Not used with sqlite3.
            'PASSWORD': '',                   # Not used with sqlite3.
            'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
        }
    }

    call_command('test_coverage', 'scielo_extensions')

if __name__ == '__main__':
    main()
