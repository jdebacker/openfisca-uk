from openfisca_core.model_api import *
from openfisca_uk.entities import *


class income_tax(Variable):
    value_type = float
    entity = Person
    label = u"Income tax paid per week"
    definition_period = ETERNITY

    def formula(person, period, parameters):
        return 0.45 * person("income_tax_applicable_amount", period)


class NI(Variable):
    value_type = float
    entity = Person
    label = u"National Insurance paid per week"
    definition_period = ETERNITY
    reference = ["https://www.gov.uk/national-insurance"]

    def formula(person, period, parameters):
        return 0.12 * person("income_tax_applicable_amount", period)


class basic_income(Variable):
    value_type = float
    entity = Person
    label = u"Amount of basic income received per week"
    definition_period = ETERNITY

    def formula(person, period, parameters):
        return person("is_adult", period) * 190

class benunit_basic_income(Variable):
    value_type = float
    entity = BenUnit
    label = u'label'
    definition_period = ETERNITY

    def formula(benunit, period, parameters):
        return benunit.sum(benunit.members("basic_income", period))

class benunit_untaxed_means_tested_bonus(Variable):
    value_type = float
    entity = BenUnit
    label = u'label'
    definition_period = ETERNITY

    def formula(person, period, parameters):
        return person("benunit_basic_income", period)


class simulation_4(Reform):
    def apply(self):
        for changed_var in [income_tax, NI, benunit_basic_income, benunit_untaxed_means_tested_bonus]:
            self.update_variable(changed_var)
        for added_var in [basic_income]:
            self.add_variable(added_var)
