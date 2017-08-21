"""Tests detection of fixed variables."""
import pyutilib.th as unittest
from pyomo.environ import (ConcreteModel, TransformationFactory,
                           value, Var)

__author__ = "Qi Chen <qichen at andrew.cmu.edu>"


class TestConstraintToVarBoundTransform(unittest.TestCase):
    """Tests detection of fixed variables."""

    def test_fixed_var_propagate(self):
        """Test for detecting de-facto fixed variables and fixing them."""
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.v2 = Var(initialize=2)
        m.v1.setub(2)
        m.v1.setlb(2)

        TransformationFactory('core.detect_fixed_vars').apply_to(m)
        self.assertTrue(m.v1.fixed)
        self.assertFalse(m.v2.fixed)

    def test_fixed_var_revert(self):
        """Test for reversion of fixed variables."""
        m = ConcreteModel()
        m.v1 = Var(initialize=1)
        m.v2 = Var(initialize=2)
        m.v1.setub(2)
        m.v1.setlb(2)

        xfrm = TransformationFactory('core.detect_fixed_vars')
        xfrm.apply_to(m, tmp=True)
        self.assertTrue(m.v1.fixed)
        self.assertFalse(m.v2.fixed)
        xfrm.revert()
        self.assertFalse(m.v1.fixed)
        self.assertEquals(value(m.v1), 1)


if __name__ == '__main__':
    unittest.main()