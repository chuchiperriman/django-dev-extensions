from django.core.management.base import AppCommand
from optparse import make_option
import os

SKELETONS = {
    'lv': '''
class {class_name}(ListView):
    model={model}
    template_name='{template_path}/{model_low}/list.html'
''',
    'cv': '''
class {class_name}(CreateView):
    model={model}
    template_name = '{template_path}/{model_low}/form.html'
    
    def get_success_url(self):
        return reverse('{app_name}-{model_low}-create')
'''
}

class Command(AppCommand):

    option_list = AppCommand.option_list + (
        make_option('--model', '-m', action='store', dest='model_name', 
                    help='The model for the View'),
        make_option('--viewtype', '-t', action='store', dest='view_type', 
                    help='The view type'),
    )

    args = "[appname]"
    label = 'application name'

    help = "Create a new view skeleton."

    def handle_app(self, app, **options):
        view_type = options['view_type']
        view_name = None
        if view_type == 'lv':
            view_name = 'ListView'
        elif view_type == 'cv':
            view_name = 'CreateView'
        else:
            raise Exception('View type incorrect (lv, cv)')
            
        class_name = '%s%s' % (options['model_name'], view_name)
        app_name = app.__name__.rsplit('.')[-2]
        app_path = app.__name__.rsplit('.', 1)[0].replace('.', '/')
        model_low=options['model_name'].lower()
        
        view = SKELETONS[view_type].format(model=options['model_name'],
            model_low=model_low,
            class_name = class_name,
            template_path=app_path.split('/')[-1],
            app_name = app_name)
            
        if not os.path.exists(app_path):
            raise Exception('App folder not found: %s' % app_path)
            
        views_path = os.path.join (app_path, 'views', model_low)
        views_file = views_path + '.py'

        if not os.path.exists(views_file):
            raise Exception('Views file not found : %s' % views_file)
        
        content = None
        
        with open(views_file, "r+") as vf:
            content = vf.read()
            found = False
            for line in content.splitlines():
                if (view_name in line) and ('import' in line):
                    found = True
                    
            if not found:
                imp = 'from django.views.generic import %s\n' % view_name
                content = imp + content
                
            if class_name in content:
                raise Exception('A view with the name %s already exists' % class_name)
                
            content += view
            
            print content
            raise NotImplementedError()
        
            vf.seek(0)
            vf.write(content)
            vf.truncate()
        
