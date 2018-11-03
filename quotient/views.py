from django.shortcuts import render
from quotient.forms import MappingClassForm

import curver

def index(request):
    order = None
    signature = None
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
    
    return render(request, 'quotient/index.html', {'form': form, 'order': order, 'signature': signature, 'version': curver.__version__})

def examples(request):
    examples = [
            (0, 5, ['s_0.s_1.s_2.s_3', 's_0.S_1.S_2.s_4']),
            (1, 1, ['a_0.b_0', 'a_0.b_0.a_0']),
            (2, 1, ['a_0.b_0.c_0.b_1']),
            ]
    
    return render(request, 'quotient/examples.html', {'examples': examples})
