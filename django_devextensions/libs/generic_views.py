from django.core.management.base import AppCommand
from optparse import make_option
import os

def get_manager_by_tag (tag):
    if tag == 'lv':
        return ListViewManager()
    elif tag == 'cv':
        return CreateViewManager()
    elif tag == 'uv':
        return UpdateViewManager()
    elif tag == 'dv':
        return DetailViewManager()
    else:
        raise Exception('View type incorrect (lv, cv, dv, uv)')

class GenericViewManager (object):
    tag = None
    view_name = None
    body = None
    
    def get_classname(self, model_name):
        return '%s%s' % (model_name, self.view_name)

    def get_generic_import(self):
        return 'from django.views.generic import %s\n' % self.view_name
        
    def get_app_name(self, app):
        return app.__name__.rsplit('.')[-2]
        
    def get_app_path(self, app):
        return app.__name__.rsplit('.', 1)[0].replace('.', '/')
        
    def get_body(self, app, model_name):
        app_name = self.get_app_name(app)
        app_path = self.get_app_path(app)
        model_low = model_name.lower()
        
        return self.body.format(model=model_name,
            model_low=model_low,
            class_name = self.get_classname(model_name),
            template_path=app_path.split('/')[-1],
            app_name = app_name)

class ListViewManager (GenericViewManager):
    tag = 'lv'
    view_name = 'ListView'
    body = '''
class {class_name}(ListView):
    model={model}
    template_name='{template_path}/{model_low}/list.html'
'''
            
class CreateViewManager (GenericViewManager):
    tag = 'cv'
    view_name = 'CreateView'
    body = '''
class {class_name}(CreateView):
    model={model}
    template_name = '{template_path}/{model_low}/form.html'
    
    def get_success_url(self):
        return reverse('{app_name}-{model_low}-detail')
'''

class UpdateViewManager (GenericViewManager):
    tag = 'uv'
    view_name = 'UpdateView'
    body = '''
class {class_name}(UpdateView):
    model={model}
    template_name = '{template_path}/{model_low}/form.html'
    
    def get_success_url(self):
        return reverse('{app_name}-{model_low}-detail')
'''

class DetailViewManager(GenericViewManager):
    tag = 'dv'
    view_name = 'DetailView'
    body = '''
class {class_name}(DetailView):
    model={model}
    template_name = '{template_path}/{model_low}/detail.html'
'''

