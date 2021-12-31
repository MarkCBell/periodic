from collections import namedtuple, defaultdict
from fractions import Fraction
import re

from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, validators, IntegerField, ValidationError

import curver

app = Flask(__name__)

ConePoint = namedtuple('ConePoint', ['punctured', 'order', 'rotation', 'preimages'])
Orbifold = namedtuple('Orbifold', ['order', 'euler_characteristic', 'cone_points'])

def cone(cp, order):
    # Rotation number is the multiplicative inverse of holonomy in ZZ/order.
    return ConePoint(cp.punctured, cp.order, 0 if min(cp.holonomy) == 0 else Fraction(min(range(1, cp.order), key=lambda i: i * min(cp.holonomy) % order), cp.order), cp.preimages)

class WordsForm(Form):
    genus = IntegerField('Genus', [validators.InputRequired()], default=1)
    punctures = IntegerField('Punctures', [validators.InputRequired()], default=1)
    words = StringField('Words', [validators.InputRequired()])

    def validate_genus(form, field):
        if field.data < 0:
            raise ValidationError('Genus must be a non-negative integer')

    def validate_punctures(form, field):
        if field.data < 1:
            raise ValidationError('Punctures must be a positive integer')

@app.route('/', methods=['POST', 'GET'])
def index():
    error = None
    order = None
    classes = defaultdict(list)
    non_periodic = []
    form = WordsForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            g, p = form.genus.data, form.punctures.data
            words = form.words.data
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
        except Exception as e:
            error = str(e)

    print(classes)
    return render_template('index.html', form=form, classes=dict(classes), non_periodic=non_periodic, version=curver.__version__, error=error)

@app.route('/examples')
def examples():
    examples = [
            (0, 5, ['s_0.s_1.s_2.s_3', 's_0.S_1.S_2.s_4']),
            (1, 1, ['a_0.b_0', 'a_0.b_0.a_0']),
            (2, 1, ['a_0.b_0.c_0.b_1']),
            ]
    
    return render_template('examples.html', examples=examples)
