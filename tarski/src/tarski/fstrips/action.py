

class Action:
    """ A (possibly lifted) planning action """

    def __init__(self, language, name, parameters, precondition, effects):
        self.name = name
        self.language = language
        self.parameters = parameters
        self.precondition = precondition
        self.effects = effects

    def dump(self):
        return dict(name=self.name,
                    params=[par.dump() for par in self.parameters],
                    precondition=self.precondition.dump(),
                    effects=[eff.dump() for eff in self.effects.dump()])

    def __str__(self):
        tokens = ['action {}:'.format(self.name),
                  'pre=({})'.format(self.precondition),
                  'eff=({})'.format(' & '.join(str(eff) for eff in self.effects))]
        return '\n'.join(tokens)
