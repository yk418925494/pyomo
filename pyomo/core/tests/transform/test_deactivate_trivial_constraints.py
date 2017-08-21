# -*- coding: UTF-8 -*-
"""Tests deactivation of trivial constraints."""
import pyutilib.th as unittest
from pyomo.environ import (Constraint, ConcreteModel, TransformationFactory,
                           Var)

__author__ = "Qi Chen <qichen at andrew.cmu.edu>"


class TestTrivialConstraintDeactivator(unittest.TestCase):
    """Tests deactivation of trivial constraints."""

    def test_deactivate_trivial_constraints(self):
        """Test for deactivation of trivial constraints."""
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.v2 = Var(initialize=2)
        m.v3 = Var(initialize=3)
        m.c = Constraint(expr=m.v1 <= m.v2)
        m.c2 = Constraint(expr=m.v2 >= m.v3)
        m.c3 = Constraint(expr=m.v1 <= 5)
        m.v1.fix()

        TransformationFactory(
            'core.deactivate_trivial_constraints').apply_to(m)
        self.assertTrue(m.c.active)
        self.assertTrue(m.c2.active)
        self.assertFalse(m.c3.active)

    def test_deactivate_trivial_constraints_revert(self):
        """Test for reversion of trivial constraint deactivation."""
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.v2 = Var(initialize=2)
        m.v3 = Var(initialize=3)
        m.c = Constraint(expr=m.v1 <= m.v2)
        m.c2 = Constraint(expr=m.v2 >= m.v3)
        m.c3 = Constraint(expr=m.v1 <= 5)
        m.v1.fix()

        xfrm = TransformationFactory(
            'core.deactivate_trivial_constraints')
        xfrm.apply_to(m, tmp=True)
        self.assertTrue(m.c.active)
        self.assertTrue(m.c2.active)
        self.assertFalse(m.c3.active)

        xfrm.revert()
        self.assertTrue(m.c3.active)

    def test_trivial_constraints_lb_conflict(self):
        """Test for violated trivial constraint lower bound."""
        self.assertRaises(ValueError, self._trivial_constraints_lb_conflict)

    def _trivial_constraints_lb_conflict(self):
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.c = Constraint(expr=m.v1 >= 2)
        m.v1.fix()
        TransformationFactory(
            'core.deactivate_trivial_constraints').apply_to(m)

    def test_trivial_constraints_ub_conflict(self):
        """Test for violated trivial constraint upper bound."""
        self.assertRaises(ValueError, self._trivial_constraints_ub_conflict)

    def _trivial_constraints_ub_conflict(self):
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.c = Constraint(expr=m.v1 <= 0)
        m.v1.fix()
        TransformationFactory(
            'core.deactivate_trivial_constraints').apply_to(m)


if __name__ == '__main__':
    unittest.main()