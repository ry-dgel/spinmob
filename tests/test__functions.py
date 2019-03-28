# -*- coding: utf-8 -*-
"""
Module for testing _data.py
"""
import os  # For loading fixtures
import numpy as _n
import spinmob as sm
_f = sm._functions

import unittest as _ut

# Not sure how to handle ~line 125 where if a path is not specified, the user
# manually enters one.  This is annoying to test.  Has to be a way to handle
# this nicely.


class Test_functions(_ut.TestCase):
    """
    Test class for databox.
    """

    def setUp(self):    return
    def tearDown(self): return
    
    def test_is_a_number(self):
        
        # Normal test
        self.assertTrue(_f.is_a_number(7))
        
        # String test (used for databox loading I believe)
        self.assertTrue(_f.is_a_number('100'))
        
        # Non-numbers
        self.assertFalse(_f.is_a_number([]))
    
    def test_fft(self):

        # Odd number of points
        f, Y = _f.fft([1,2,3,4,5],[1,2,1,2,1])
        self.assertEqual(f[0],-0.4)
        self.assertEqual(f[-1],0.4)
        self.assertAlmostEqual(Y[0],-0.1+0.30776835j)
        self.assertAlmostEqual(Y[2],1.4)

        # Even number of points
        f, Y = _f.fft([1,2,3,4],[1,2,1,2])
        self.assertEqual(f[0],-0.5)
        self.assertEqual(f[-1],0.25)
        self.assertAlmostEqual(Y[0],-0.5)
        self.assertAlmostEqual(Y[2],1.5)
        
    
    def test_psd(self):

        # Odd number of points
        t    = _n.linspace(0,10,101)
        y    = _n.cos(t) + 1
        f, P = _f.psd(t,y)
        
        # Integral test
        self.assertAlmostEqual(sum(P)*(f[1]-f[0]), _n.average(y**2))

        # Even number of points
        t    = _n.linspace(0,10,100)
        y    = _n.cos(t) + 1
        f, P = _f.psd(t,y)
        
        # Integral test
        self.assertAlmostEqual(sum(P)*(f[1]-f[0]), _n.average(y**2))
    
        # Windowed, pow2
        t    = _n.linspace(0,10,100)
        y    = _n.cos(5*t) + 1
        f, P = _f.psd(t,y,pow2=True,window='hanning')
        
        # Integral test
        self.assertAlmostEqual(sum(P)*(f[1]-f[0]), _n.average( (y[0:64]*_n.hanning(64))**2))


        # Windowed, pow2, rescaled
        t    = _n.linspace(0,10,100)
        y    = _n.cos(5*t) + 1
        f, P = _f.psd(t,y,pow2=True,window='hanning',rescale=True)
        
        # Integral test
        self.assertAlmostEqual(sum(P)*(f[1]-f[0]), _n.average( y[0:64]**2))

    
        # DC and nyquist component test
        f, P = _f.psd([1,2,3,4],[1,2,1,2])
        self.assertEqual(( P[0]*(f[1]-f[0]))**0.5, 1.5)
        self.assertEqual((P[-1]*(f[1]-f[0]))**0.5, 0.5)
        
        # Middle frequency component test
        f, P = _f.psd([1,2,3,4],[1,2,2,1])
        self.assertAlmostEqual((P[0]*(f[1]-f[0]))**0.5, 1.5)
        self.assertAlmostEqual((P[1]*(f[1]-f[0]))**0.5, 0.5)
        
    def test_generate_fake_data(self):
        
        # Survival test
        _f.generate_fake_data('cos(x)*3',_n.linspace(-5,5,11),1,2)
    
    def test_coarsen_data(self):
        
        # Simple coarsen
        a = sm.fun.coarsen_data([1,2,3,4,5],[1,2,1,2,1])
        self.assertEqual(_n.shape(a), (2,2))
        self.assertEqual(a[1][1], 1.5)
    
        # With ey float
        a = sm.fun.coarsen_data([1,2,3,4,5],[1,2,1,2,1],2,level=3)
        self.assertEqual(_n.shape(a), (3,1))
        self.assertAlmostEqual(a[2][0], 1.15470054)
        
        # With ey array
        a = sm.fun.coarsen_data([1,2,3,4,5],[1,2,1,2,1],[1,2,3,4,5],level=2)
        self.assertEqual(_n.shape(a), (3,2))
        self.assertAlmostEqual(a[2][0], 1.118033988749895)
        
        # With ex and ey
        a = sm.fun.coarsen_data([1,2,3,4,5],[1,2,1,2,1],[1,2,3,4,5],[1,2,1,2,1],level=2)
        self.assertEqual(_n.shape(a), (4,2))
        self.assertAlmostEqual(a[3][1], 1.118033988749895)
        
        # Exponential coarsen simple
        a = sm.fun.coarsen_data(_n.linspace(0,100,100),_n.linspace(100,0,100),exponential=True)
        self.assertEqual(_n.shape(a), (2,7))
        self.assertAlmostEqual(a[1][5], 52.02020202020202)
        
        # Exponential coarsen ex and ey
        a = sm.fun.coarsen_data(_n.linspace(0,100,100),_n.linspace(100,0,100),
                                _n.linspace(1,2,100), 3, 1.3, exponential=True)
        self.assertEqual(_n.shape(a), (4,16))
        self.assertAlmostEqual(a[3][5], 2.1213203435596424)
        
        
    

if __name__ == "__main__": _ut.main()
