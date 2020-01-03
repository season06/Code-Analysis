from django.http import HttpResponse
from django.shortcuts import render
from .process import Analysis

# render(request, template_name, dictionary)
def home(request):
    return render(request, 'home.html')

def analysis(request):
    code = {}
    if request.POST:
        model = Analysis(request.POST['code'])
        if model.code!='':
            code = str(model.code)
            model.code = model.code.replace("\r","").replace("\t","").strip()
            model.generate_diagram()
            img = 'diagram.png'
            return render(request, 'diagram.html', {'image': img, 'code_field': code})
        else:
            code = '!! Please Input Code !!'
            return render(request, 'home.html', {'code_field': code})
    