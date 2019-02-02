from django.shortcuts import render
from quotient.forms import MappingClassForm

from collections import namedtuple, defaultdict
from fractions import Fraction
import re

import curver

ConePoint = namedtuple('ConePoint', ['punctured', 'order', 'rotation', 'preimages'])
Orbifold = namedtuple('Orbifold', ['order', 'euler_characteristic', 'cone_points'])

def cone(cp, order):
    # Rotation number is the multiplicative inverse of holonomy in ZZ/order.
    return ConePoint(cp.punctured, cp.order, 0 if min(cp.holonomy) == 0 else Fraction(min(range(1, cp.order), key=lambda i: i * min(cp.holonomy) % order), cp.order), cp.preimages)

def index(request):
    error = None
    order = None
    classes = defaultdict(list)
    non_periodic = []
    if request.method == 'POST':
        form = MappingClassForm(request.POST)
        if form.is_valid():
            try:
                g = int(form.cleaned_data['genus'])
                p = int(form.cleaned_data['punctures'])
                words = form.cleaned_data['words']
                S = curver.load(g, p)
                for word in re.split('[;,]+', words):
                    h = S(word)
                    order = h.order()
                    if order == 0:
                        non_periodic.append(word)
                    else:
                        signature = h.subgroup().quotient_orbifold_signature()[0]
                        signature = Orbifold(order, signature.euler_characteristic, tuple(sorted([cone(cp, order) for cp in signature.cone_points])))
                        classes[signature].append(word)
            except NameError as e:
                error = str(e)
    else:
        form = MappingClassForm()
    
    return render(request, 'quotient/index.html', {'form': form, 'error': error, 'classes': dict(classes), 'non_periodic': non_periodic, 'version': curver.__version__})

def examples(request):
    examples = [
            (0, 5, ['s_0.s_1.s_2.s_3', 's_0.S_1.S_2.s_4']),
            (1, 1, ['a_0.b_0', 'a_0.b_0.a_0']),
            (2, 1, ['a_0.b_0.c_0.b_1']),
            ]
    
    return render(request, 'quotient/examples.html', {'examples': examples})
