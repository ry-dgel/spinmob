# -*- coding: utf-8 -*-
"""
Module for testing _data.py
"""
import os      as _os # For loading fixtures
import numpy   as _n
import spinmob as _s

import unittest as _ut

a = b = c = d = None

class Test_databox(_ut.TestCase):
    """
    Test class for databox.
    """

    def setUp(self):
        """
        Load data
        """
        # Path to the spinmob module
        self.data_path = _os.path.join(_os.path.dirname(_s.__file__), '_tests', 'fixtures', 'data_files')

    def tearDown(self):
        """
        """
        return

    def test_load_file(self):
        d = _s.data.databox()
        d.load_file(path=_os.path.join(self.data_path, 'basic.dat'))
        self.assertEqual(d[0][0], 85.0)

    def test_default_delimiter(self):
        d = _s.data.databox()
        self.assertEqual(d.delimiter, None)

    def test_set_delimiter(self):
        d = _s.data.databox(delimiter=',')
        self.assertEqual(d.delimiter, ',')

    def test_autoload_csv(self):
        """
        Test loading a CSV file
        """
        d = _s.data.load(path=_os.path.join(self.data_path, "comma.dat"))
        self.assertEqual(d[0][1], 90.0)
        self.assertEqual(d.delimiter, ',')

    def test_autoload_semicolon(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "semicolon.dat"))
        self.assertEqual(d[0][1], 90.0)
        self.assertEqual(d.delimiter, ';')

    def test_pop_data_point(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        
        # length
        l = len(d[0])
        
        # Check a value of the loaded file, first level
        val = d.pop_data_point(3)

        # The expected response
        exp = [100.0, 2.43]
        self.assertEqual(val, exp)
        self.assertEqual(len(d[0]), l-1)

    def test_execute_script(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        
        val = d.execute_script('3.0 + x/y - self[0] where x=2.0*c(0); y=c(1)')
        val = _n.around(val, 1)  # Round to 1 decimal place
        val = val.tolist()  # Convert numpy array to a list
        val = val[0:5]   # Just check the first five elements

        exp = [993.9, 713.0, 70.4, -14.7, -51.6]
        self.assertListEqual(val, exp)

    def test___len__(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        val = d.__len__()
        exp = 2
        self.assertEqual(val, exp)

    def test___setitem___str(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        d.__setitem__(0, 'test_item')
        val = d[0]
        exp = 'test_item'
        self.assertEqual(val, exp)

    def test___setitem___int(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        d.__setitem__(2, [78, 87])
        val = d[2]
        val = val.tolist()
        exp = [78, 87]
        self.assertListEqual(val, exp)

    def test___getslice__(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "basic.dat"))
        val = d[0:1]
        val = val[0]
        val = val.tolist()
        val = val[0:5]   # Just check the first five elements
        exp = [85.0, 90.0, 95.0, 100.0, 105.0]
        self.assertListEqual(val, exp)

    def test_h_str(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "headers.dat"))
        val = d.h('header1')
        exp = 'value1'
        self.assertEqual(val, exp)

    def test_h_GoodFragment(self):
        """
        This should have spinmob print out an error message.

        TODO: possible better way of handling/collecting this error message
        while testing.
        """
        d = _s.data.load(path=_os.path.join(self.data_path, "headers.dat"))
        val = d.h('header')
        exp = 'value1'
        self.assertEqual(val, exp)

    def test_pop_column_ckey(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "headers.dat"))
        val = d.pop_column('x_data')
        val = val.tolist()
        val = val[0:5]   # Just check the first five elements
        exp = [85.0, 90.0, 95.0, 100.0, 105.0]
        self.assertListEqual(val, exp)

    def test_pop_column_int(self):
        d = _s.data.load(path=_os.path.join(self.data_path, "headers.dat"))
        val = d.pop_column(0)
        val = val.tolist()
        val = val[0:5]   # Just check the first five elements
        exp = [85.0, 90.0, 95.0, 100.0, 105.0]
        self.assertListEqual(val, exp)

    def test_pop_column_neg(self):
        """
        Test spinmob error message for looking for a column that does not exist

        TODO: better way to collect these error messsages.
        """
        d = _s.data.load(path=_os.path.join(self.data_path, "headers.dat"))
        val = d.pop_column(-2)
        val = val.tolist()
        val = val[0:5]   # Just check the first five elements
        exp = [85.0, 90.0, 95.0, 100.0, 105.0]
        self.assertListEqual(val, exp)

    def test_load_single_row(self):
        """
        Test that a file with a single row of data can be loaded.
        """
        d = _s.data.load(path=_os.path.join(self.data_path, "one_row.dat"))
        
        # TODO: need a better test that only tests the load.
        value = d[0][0]
        expected_value = 85.0
        self.assertEqual(value, expected_value)

    def test_load_single_column_of_data(self):
        """
        Test that a file with a single column of data can be loaded.
        """
        d = _s.data.load(path=_os.path.join(self.data_path, 'one_column.dat'))

        value = d[0].tolist()
        expected_value = [85., 42.]
        self.assertListEqual(value, expected_value)

    def test_load_save_binary(self):
        global d
        
        # Start clean.
        if _os.path.exists('test_binary.txt'):        _os.remove('test_binary.txt')
        if _os.path.exists('test_binary.txt.backup'): _os.remove('test_binary.txt.backup')

        # Write a confusing binary file.
        d = _s.data.databox(delimiter=',')
        d.h(poo = 32)
        d['pants']       = [1,2,3,4,5]
        d['shoes,teeth'] = [1,2,1]
        d.save_file('test_binary', '*.txt', 'txt', binary='float16')
        
        # Crash tests
        print()
        d.h()
        d.c()
        
        # Load said binary
        d = _s.data.load('test_binary.txt')
        self.assertEqual(len(d), 2)
        self.assertEqual(len(d[1]), 3)
        self.assertEqual(len(d[0]), 5)
        self.assertEqual(len(d.hkeys), 2)
        
        # Do the same with no delimiter
        d = _s.data.databox(delimiter=None)
        d.h(poo = 32)
        d['pants']       = [1,2,3,4,5]
        d['shoes,teeth'] = [1,2,1]
        d.save_file('test_binary.txt',binary='float16')
        
        # Load said binary
        d = _s.data.load('test_binary.txt')
        self.assertEqual(len(d), 2)
        self.assertEqual(len(d[1]), 3)
        self.assertEqual(len(d[0]), 5)
        self.assertEqual(len(d.hkeys), 2)
        self.assertEqual(d.delimiter,'\t')

        # Clean up again.
        if _os.path.exists('test_binary.txt'): _os.remove('test_binary.txt')
        if _os.path.exists('test_binary.txt.backup'): _os.remove('test_binary.txt.backup')

        # Now modify it and save again.
        d.h(SPINMOB_BINARY='int64', test=['1,2,3,4',1,2,3,4])
        d['new_column'] = [44]
        d.delimiter = None
        d.save_file('test_binary.txt')
        
        # Load it again
        d = _s.data.load('test_binary.txt')
        self.assertEqual(len(d.ckeys), 3)
        self.assertEqual(len(d.hkeys), 3)
        self.assertEqual(len(d[2]),    1)
        self.assertEqual(d[1][1],      2)
        
        # Clean up.
        if _os.path.exists('test_binary.txt'): _os.remove('test_binary.txt')
        if _os.path.exists('test_binary.txt.backup'): _os.remove('test_binary.txt.backup')

        # Load the difficult one to encode
        d = _s.data.load(path=_os.path.join(self.data_path, "difficult.binary"))
        self.assertEqual(_n.shape(d), (6,500))
        self.assertAlmostEqual(d[4][4], 0.062340055)
        

        # Load another difficult one
        d = _s.data.load(path=_os.path.join(self.data_path, "float16.binary"))
        self.assertEqual(_n.shape(d), (6,500))
        self.assertEqual(d[4][4], _n.float16(0.062347))
        
        

    def test_is_same_as(self):
        global a, b, c
        
        # Create databoxes
        a = _s.data.databox()
        b = _s.data.databox()
        c = _s.data.databox()
        
        # Add headers
        a.h(x=3,y=4)
        a['t'] = [1,2,3]
        a['y'] = [1,2,1]
        
        # Some non-thorough self tests 
        self.assertTrue(a.is_same_as(a, headers=True, 
                                             columns=True, 
                                             header_order=True, 
                                             column_order=True, 
                                             ckeys=True))
        
        self.assertTrue(a.is_same_as(a, headers=True, 
                                             columns=True, 
                                             header_order=False, 
                                             column_order=False, 
                                             ckeys=False))
        
        # Wrong number of elements
        b.h(y=4)
        b['y'] = [1,2,1]
        self.assertFalse(a.is_same_as(b, headers=True, 
                                              columns=True, 
                                              header_order=True, 
                                              column_order=True, 
                                              ckeys=True))
        self.assertFalse(a.is_same_as(b, headers=False, 
                                              columns=True, 
                                              header_order=True, 
                                              column_order=True, 
                                              ckeys=True))
        self.assertFalse(a.is_same_as(b, headers=True, 
                                              columns=False, 
                                              header_order=True, 
                                              column_order=True, 
                                              ckeys=True))
        
        # Wrong order
        b.h(x=3)
        b['t'] = [1,2,3]
        self.assertFalse(a.is_same_as(b, headers=True, 
                                             columns=True, 
                                             header_order=True, 
                                             column_order=True, 
                                             ckeys=True))
        self.assertFalse(a.is_same_as(b, headers=True, 
                                             columns=True, 
                                             header_order=False, 
                                             column_order=True, 
                                             ckeys=True))
        self.assertFalse(a.is_same_as(b, headers=True, 
                                             columns=True, 
                                             header_order=True, 
                                             column_order=False, 
                                             ckeys=True))
        self.assertTrue(a.is_same_as(b, headers=True, 
                                             columns=True, 
                                             header_order=False, 
                                             column_order=False, 
                                             ckeys=True))
        
        # no ckeys, just numbers
        self.assertFalse(a.is_same_as(b, headers=True, 
                                              columns=True, 
                                              header_order=True, 
                                              column_order=True, 
                                              ckeys=False))
        
        # Column value different
        b[1][2]=47
        self.assertFalse(a.is_same_as(b, headers=True, 
                                              columns=True, 
                                              header_order=False, 
                                              column_order=False, 
                                              ckeys=True))
        self.assertTrue(a.is_same_as(b,  headers=True, 
                                              columns=False, 
                                              header_order=False, 
                                              column_order=False, 
                                              ckeys=True))
        
        # Header value different
        a.h(x=4)
        self.assertFalse(a.is_same_as(b, headers=True, 
                                              columns=False, 
                                              header_order=False, 
                                              column_order=False, 
                                              ckeys=True))
        
        # == symbol => identical
        c.copy_all(a)
        self.assertTrue(a==c)
        self.assertFalse(a is c)
        
        # Compare with another type
        self.assertFalse(a.is_same_as(None))
    
    
    def test_load_dialogs(self):
        
        # Crash tests
        _s.data.load(text='CANCEL ME')
        _s.data.load_multiple(text='CANCEL ME')

        
if __name__ == "__main__":
    _ut.main()
