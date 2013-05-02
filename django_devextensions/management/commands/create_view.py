from django.core.management.base import AppCommand
from optparse import make_option
import os

SKELETON = '''
class {class_name}(ListView):
    model={model}
    template_name='{template_path}/{model_low}/list.html'
'''

class Command(AppCommand):

    option_list = AppCommand.option_list + (
        make_option('--model', '-m', action='store', dest='model_name', 
                    help='The name to use for the management command'),
    )

    args = "[appname]"
    label = 'application name'

    help = "Create a new view skeleton."

    def handle_app(self, app, **options):
        
        app_path = app.__name__.rsplit('.', 1)[0].replace('.', '/')
        model_low=options['model_name'].lower()
        class_name = '%sListView' % options['model_name']
        
        view = SKELETON.format(model=options['model_name'],
            model_low=model_low,
            class_name = class_name,
            template_path=app_path.split('/')[-1])
            
        if not os.path.exists(app_path):
            raise Exception('App folder not found: %s' % app_path)
            
        views_path = os.path.join (app_path, 'views', model_low)
        views_file = views_path + '.py'

        if not os.path.exists(views_file):
            raise Exception('Views file not found : %s' % views_file)
        
        content = None
        with open(views_file, "r+") as vf:
            content = vf.read()
            if not ('import ListView' in content):
                content = 'from django.views.generic import ListView\n' + content
                
            if class_name in content:
                raise Exception('A view with the name %s already exists' % class_name)
                
            content += view
            
            vf.seek(0)
            vf.write(content)
            vf.truncate()
        
        raise NotImplementedError()
        
        
