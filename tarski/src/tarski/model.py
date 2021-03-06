# -*- coding: utf-8 -*-
from collections import defaultdict

from . import errors as err
from .syntax import Function, Constant, TermReference
from .syntax.predicate import Predicate


def _check_assignment(fun, point, value=None):
    assert isinstance(point, tuple)

    elements = point + (value,) if value is not None else point
    processed = []

    typ = fun.sort

    if len(typ) != len(elements):
        raise err.ArityMismatch(fun, elements)

    language = fun.language
    for element, expected_type in zip(elements, typ):

        if not isinstance(element, Constant):
            # Assume a literal value has been passed instead of its corresponding constant
            element = Constant(expected_type.cast(element), expected_type)
            # raise err.IncorrectExtensionDefinition(fun, point, value)

        if element.language != language:
            raise err.LanguageMismatch(element, element.language, language)

        if not language.is_subtype(element.sort, expected_type):
            raise err.SortMismatch(element, element.sort, expected_type)

        processed.append(element)

    if value is None:
        return tuple(processed)

    assert len(processed) > 0
    return tuple(processed[:-1]), processed[-1]


class Model:
    """ A First Order Language Model """

    def __init__(self, language):
        self.evaluator = None
        self.language = language
        self.function_extensions = dict()
        self.predicate_extensions = defaultdict(set)

    def set(self, fun, *args):
        """ Set the value of function 'fun' at point 'point' to be equal to 'value'
            'point' needs to be a tuple of constants, and value a single constant.
        """
        if not isinstance(fun, Function):
            raise err.SemanticError("Model.set() can only set the value of functions")
        point, value = args[:-1], args[-1]
        point, value = _check_assignment(fun, point, value)
        if fun.signature not in self.function_extensions:
            definition = self.function_extensions[fun.signature] = ExtensionalFunctionDefinition()
        else:
            definition = self.function_extensions[fun.signature]
            if not isinstance(definition, ExtensionalFunctionDefinition):
                raise err.SemanticError("Cannot define extension of intensional definition")

        definition.set(point, value)

    def add(self, predicate: Predicate, *args):
        if not isinstance(predicate, Predicate):
            raise err.SemanticError("Model.add() can only set the value of predicates")
        point = _check_assignment(predicate, args)
        self.predicate_extensions[predicate.signature].add(wrap_tuple(point))

    def remove(self, predicate: Predicate, *args):
        self.predicate_extensions[predicate.signature].remove(wrap_tuple(args))

    def value(self, fun: Function, point):
        """ Return the value of the given function on the given point in the current model """
        definition = self.function_extensions[fun.signature]
        return definition.get(point)

    def holds(self, predicate: Predicate, point):
        """ Return true iff the given predicate is true on the given point in the current model """
        # return tuple(c.symbol for c in point) in self.predicate_extensions[predicate.signature]
        return wrap_tuple(point) in self.predicate_extensions[predicate.signature]

    def list_all_extensions(self):
        """ Return a mapping between predicate and function signatures and a list of all their respective extensions.
        This list *unwraps* the TermReference's used internally in this class back into plain Tarski terms, so that
        you can rely on the returned extensions being made up of Constant's, Variables, etc., not TermReference's
        """
        exts = {k: [unwrap_tuple(ref) for ref in refs] for k, refs in self.predicate_extensions.items()}
        exts.update(
            (k, [unwrap_tuple(point) + (value, ) for point, value in ext.data.items()]) for k, ext in self.function_extensions.items())
        return exts

    def __getitem__(self, arg):
        try:
            expr, sigma = arg
            return self.evaluator(expr, self, sigma)
        except TypeError:
            return self.evaluator(arg, self)


def create(lang):
    return Model(lang)


class ExtensionalFunctionDefinition:
    def __init__(self):
        self.data = dict()

    def set(self, point, value):
        assert isinstance(point, tuple)
        assert isinstance(value, Constant)
        self.data[wrap_tuple(point)] = value

    def get(self, point):
        return self.data[wrap_tuple(point)]


# class IntensionalFunctionDefinition:
#     pass

def wrap_tuple(tup):
    """ Create a tuple of Term references from a tuple of terms """
    return tuple(TermReference(a) for a in tup)


def unwrap_tuple(tup):
    """ Create a tuple of Tarski terms from a tuple of Term references"""
    return tuple(ref.term for ref in tup)
