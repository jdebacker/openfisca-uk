from openfisca_core.model_api import *
from openfisca_uk.entities import *
import os

dir_name = os.path.dirname(__file__)


def modify_parameters(parameters):
    file_path = os.path.join(
        dir_name, "parameters", "simulation_2", "new_income_tax.yaml"
    )
    reform_parameters_subtree = load_parameter_file(
        file_path, name="new_income_tax"
    )
    parameters.taxes.income_tax.add_child(
        "new_income_tax", reform_parameters_subtree
    )
    return parameters


class income_tax(Variable):
    value_type = float
    entity = Person
    label = u"Income tax paid per week"
    definition_period = ETERNITY

    def formula(person, period, parameters):
        estimated_yearly_income = (person("income_tax_applicable_amount", period)) * 52
        weekly_tax = (
            parameters(period).taxes.income_tax.new_income_tax.calc(
                estimated_yearly_income
            )
        ) / 52
        return weekly_tax


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
        adult_young = (person("age", period) >= 16) * (
            person("age", period) < 24
        )
        adult_old = (person("age", period) >= 24) * (
            person("age", period) < 65
        )
        return (
            person("is_senior", period) * 50
            + adult_young * 55
            + adult_old * 65
            + person("is_child", period) * 22
        )

class benunit_basic_income(Variable):
    value_type = float
    entity = BenUnit
    label = u'label'
    definition_period = ETERNITY

    def formula(benunit, period, parameters):
        return benunit.sum(benunit.members("basic_income", period))


class benunit_non_means_tested_bonus(Variable):
    value_type = float
    entity = BenUnit
    label = u'label'
    definition_period = ETERNITY

    def formula(person, period, parameters):
        return min_(25, person("benunit_basic_income", period))

class benunit_untaxed_means_tested_bonus(Variable):
    value_type = float
    entity = BenUnit
    label = u'label'
    definition_period = ETERNITY

    def formula(person, period, parameters):
        return max_(0, person("benunit_basic_income", period) - 25)


class simulation_2(Reform):
    def apply(self):
        self.modify_parameters(modify_parameters)
        for changed_var in [
            income_tax,
            NI,
            benunit_basic_income,
            benunit_untaxed_means_tested_bonus,
            benunit_non_means_tested_bonus,
        ]:
            self.update_variable(changed_var)
        for added_var in [basic_income]:
            self.add_variable(added_var)
