from django.shortcuts import render
from quotient.forms import MappingClassForm

from collections import namedtuple
from fractions import Fraction

import curver

ConePoint = namedtuple('ConePoint', ['punctured', 'order', 'rotation', 'preimages'])
Orbifold = namedtuple('Orbifold', ['euler_characteristic', 'preimages', 'cone_points'])

def index(request):
    error = None
    order = None
    signature = None
    if request.method == 'POST':
        form = MappingClassForm(request.POST)
        if form.is_valid():
            try:
                g = int(form.cleaned_data['genus'])
                p = int(form.cleaned_data['punctures'])
                word = form.cleaned_data['word']
                h = curver.load(g, p)(word)
                order = h.order()
                if order == 0:
                    signature = None
                else:
                    signature = h.subgroup().quotient_orbifold_signature()[0]
                    signature = Orbifold(signature.euler_characteristic, 1, sorted([
                        ConePoint(cp.punctured, cp.order, 0 if min(cp.holonomy) == 0 else Fraction(min(range(1, cp.order), key=lambda i: i * min(cp.holonomy) % order), cp.order), cp.preimages) for cp in signature.cone_points]))
            except Exception as e:
                error = str(e)
    else:
        form = MappingClassForm()
    
    return render(request, 'quotient/index.html', {'form': form, 'error': error, 'order': order, 'signature': signature, 'version': curver.__version__})

def examples(request):
    examples = [
            (0, 5, ['s_0.s_1.s_2.s_3', 's_0.S_1.S_2.s_4']),
            (1, 1, ['a_0.b_0', 'a_0.b_0.a_0']),
            (2, 1, ['a_0.b_0.c_0.b_1']),
            ]
    
    return render(request, 'quotient/examples.html', {'examples': examples})
