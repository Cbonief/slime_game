# #
# requerimentos = {
#     'Level': 2,
#     'Força': 3
# }


class Skill:

    def __init__(self, name, requirements, ):
        self.requirements = requirements

    def verify(self, character):
        meets_requirements = True
        for [requirement_type, value] in self.requirements.items():
            if not (requirement_type == 'Level' and character.level > value):
                meets_requirements = False
            for [attribute, attribute_value] in self.character.attributes.items():
                if not (requirement_type == attribute and attribute_value > value):
                    meets_requirements = False
        return meets_requirements
