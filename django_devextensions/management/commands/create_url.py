from django.core.management.base import AppCommand
from optparse import make_option
import os
from django_devextensions.libs.generic_views import get_manager_by_tag

class Command(AppCommand):

    option_list = AppCommand.option_list + (
        make_option('--model', '-m', action='store', dest='model_name', 
                    help='The model for the View'),
        make_option('--viewtype', '-t', action='store', dest='view_type', 
                    help='The view type'),
    )

    args = "[appname]"
    label = 'application name'

    help = "Create a new url skeleton."

    def handle_app(self, app, **options):
        view_type = options['view_type']
        model_name = options['model_name']
        manager = get_manager_by_tag(view_type)
        
        print manager.get_url_template(app, model_name)
