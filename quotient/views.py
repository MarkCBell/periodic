from django.shortcuts import render
from quotient.forms import MappingClassForm
# Create your views here.
from django.http import HttpResponse

import curver

def index(request):
    if request.method == 'POST':
        form = MappingClassForm(request.POST)
        if form.is_valid():
            g = int(form.cleaned_data['genus'])
            p = int(form.cleaned_data['punctures'])
            word = form.cleaned_data['word']
            h = curver.load(g, p)(word)
            order = h.order()
            signature = h.quotient_orbifold_signature()[0] if order > 0 else None
    else:
        form = MappingClassForm()
        order = None
        signature = None
    
    return render(request, 'quotient/index.html', {'form': form, 'order': order, 'signature': signature, 'version': curver.__version__})

