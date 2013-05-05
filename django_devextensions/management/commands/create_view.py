from django.core.management.base import AppCommand
from optparse import make_option
import os
from django_devextensions.libs.generic_views import get_manager_by_tag

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
        return reverse('{app_name}-{model_low}-detail')
''',
    'uv': '''
class {class_name}(UpdateView):
    model={model}
    template_name = '{template_path}/{model_low}/form.html'
    
    def get_success_url(self):
        return reverse('{app_name}-{model_low}-detail')
''',
    'dv': '''
class {class_name}(DetailView):
    model={model}
    template_name = '{template_path}/{model_low}/detail.html'
''',
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
        model_name = options['model_name']
        manager = get_manager_by_tag(view_type)
        class_name = manager.get_classname(model_name)
        app_path = manager.get_app_path(app)
        body = manager.get_body(app, model_name)
            
        if not os.path.exists(app_path):
            raise Exception('App folder not found: %s' % app_path)
            
        views_path = os.path.join (app_path, 'views', model_name.lower())
        views_file = views_path + '.py'

        if not os.path.exists(views_file):
            raise Exception('Views file not found : %s' % views_file)
        
        content = None
        
        with open(views_file, "r+") as vf:
            content = vf.read()
            found = False
            for line in content.splitlines():
                if (manager.view_name in line) and ('import' in line):
                    found = True
                    
            if not found:
                content = manager.get_generic_import() + content
                
            if class_name in content:
                raise Exception('A view with the name %s already exists' % class_name)
                
            content += body
            
            #print content
            #raise NotImplementedError()
        
            vf.seek(0)
            vf.write(content)
            vf.truncate()
        
