#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 10:18:53 2018

@author: ashkar
"""

import unittest
import csvPreProcessCommented

class TestcsvPreProcessCommented(unittest.TestCase):
    
    def test_isEveryElementEmpty(self):
        result = csvPreProcessCommented.isEveryElementEmpty(["13", "46", "asd0", "", "c"])
        self.assertEqual(result, [False])
        
    def test_isExistsDuplicate(self):
        result = csvPreProcessCommented.isExistsDuplicate([" ", "", "bla", ""])
        self.assertEqual(result, [False, 0, [2], ["bla"]])
        
        result = csvPreProcessCommented.isExistsDuplicate(["das", "", "  ", "das"])
        self.assertEqual(result, [False, 1])
        
    def test_isExistsNullHeader_s_MidWay(self):
        result = csvPreProcessCommented.isExistsNullHeader_s_MidWay(["", "asdsa", "", "    ", " ", "ds"], 2)
        self.assertEqual(result, [True])
        
        result1 = csvPreProcessCommented.isExistsNullHeader_s_MidWay(["", "asdsa", " ", "    ", " ", "ds"], 2)
        self.assertEqual(result1, [True])
        
        result2 = csvPreProcessCommented.isExistsNullHeader_s_MidWay(["", "asdsa", " ", "    ", " ", ""], 2)
        self.assertEqual(result2, [False])
        
    def test_isAgainstHeaderIndices(self):
        result = csvPreProcessCommented.isAgainstHeaderIndices(["fgh", "ert", " " , "", "3123", "e32e"], [1,2,3,4,5], ["not updated","not updated","not updated","not updated"])
        self.assertEqual(result, [True, [], ["not updated","not updated","not updated","not updated"]])
        
    
        
if __name__ == "__main__":
    unittest.main()