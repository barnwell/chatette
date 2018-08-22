#!/usr/bin/env python3

from random import randint

from Generator import randomly_change_case

EMPTY_GEN = {
    "text": "",
    "entities": [],
}


def cast_to_unicode(any):
    if sys.version_info[0] == 3:
        return any
    if isinstance(any, str):
        return unicode(any, "utf-8")
    elif isinstance(any, dict):
        cast_dict = dict()
        for key in any:
            cast_key = cast_to_unicode(key)
            cast_value = cast_to_unicode(any[key])
            cast_dict[cast_key] = cast_value
        return cast_dict
    elif isinstance(any, list):
        cast_list = []
        for e in any:
            cast_list.append(cast_to_unicode(e))
        return cast_list
    else:
        return any


def randomly_change_case(text):
    """Randomly set the case of the first letter of `text`"""
    if randint(0, 99) >= 50:
        return with_leading_lower(text)
    else:
        return with_leading_upper(text)
def with_leading_upper(text):
    """Returns `text` with a leading uppercase letter"""
    for (i, c) in enumerate(text):
        if not c.isspace():
            return text[:i] + text[i].upper() + text[(i+1):]
    return text
def with_leading_lower(text):
    """Returns `text` with a leading lowercase letter"""
    for (i, c) in enumerate(text):
        if not c.isspace():
            return text[:i] + text[i].upper() + text[(i+1):]
    return text


def may_get_leading_space(text):
    return (text != "" and not text.startswith(' '))


class UnitDefinition():
    """Superclass representing a unit definition"""
    def __init__(self, name, rules=[], arg=None, casegen=False):
        self.type = "unit"

        self.name = name
        self.rules = rules
        self.argument_identifier = arg

        self.variations = dict()

        self.casegen = casegen


    def add_rule(self, rule, variation_name=None):
        if variation_name is None:
            self.rules.append(rule)
        else:
            if variation_name == "":
                raise SyntaxError("Defining a "+self.type+" with an empty name"+
                    "is not allowed")
            if variation_name not in self.variations:
                self.variations[variation_name] = [rule]
            else:
                self.variations[variation_name].append(rule)
            self.rules.append(rule)

    def generate_random(self, variation_name=None, arg_value=None):
        """
        Generates one of your rule at random and
        returns the string generated and the entities inside it
        """
        chosen_rule = None
        if variation_name is None:
            chosen_rule = self.rules[randint(0,len(self.rules)-1)]
        else:
            if variation_name not in self.variations:
                raise SyntaxError("Couldn't find a variation named '"+
                    variation_name+"' for "+self.type+" '"+self.name+"'")
            chosen_rule = \
                self.rules[randint(0, len(self.variations[variation_name])-1)]
        (text, entities) = chosen_rule.generate(arg_value)
        if self.casegen:
            text = randomly_change_case(text)
        return (text, entities)

    def generate_all(self):
        pass  # TODO


class TokenModel():
    """
    Represents anything that can be inside a rule:
    for words and word groups, it generates as is;
    for units, it is a link to a definition that can be generated.
    """
    def __init__(self, name, leading_space=False, variation=None, arg_value=None,
        casegen=False, randgen=False, percentage_gen=50, parser=None):
            self.name = name
            self.variation = variation
            self.arg_value = arg_value

            self.casegen = casegen
            self.randgen = randgen
            self.percentgen = percentage_gen

            self.parser = parser

    def generate_random(self):
        """
        Returns a string and its entities randomly generated from the rules the
        object represents. May return an empty string if `randgen` is enabled.
        """
        # () -> {"text": str, "entities": [str]}
        pass