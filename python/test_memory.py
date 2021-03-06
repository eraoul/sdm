#!/usr/bin/env python

import unittest
import subprocess, os
from numpy import array
import sdm
from sdm import Bitstring, Hardlocation

class MemoryTestCase(unittest.TestCase):

    def setUp(self):
        sdm.initialize()

    def tearDown(self):
        sdm.free()
    
    def _memused(self):
        p = subprocess.Popen("ps -p %d -o rss | grep '^ *[0-9]\+ *$'" % os.getpid(), shell=True, stdout=subprocess.PIPE)
        return int(p.communicate()[0])

    def test_saveload(self):
        a = Bitstring()
        #sdm.initialize()
        sdm.thread_write(a, a)
        self.assertEqual(a.distance_to(sdm.thread_read(a)), 0)
        self.assertEqual(sdm.save_to_file('_test.sdm'), 0)
        sdm.free()
        sdm.initialize()
        self.assertTrue(a.distance_to(sdm.read(a)) > 0)
        sdm.free()
        self.assertEqual(sdm.initialize_from_file('_test.sdm'), 0)
        self.assertEqual(a.distance_to(sdm.thread_read(a)), 0)
        #sdm.free()

    def test_initialize_free(self, qty=5):
        sdm.free()
        m0 = self._memused()
        for i in range(qty):
            sdm.initialize()
            sdm.free()
        m1 = self._memused()
        self.assertTrue(m1 < 40000)
        sdm.initialize()

    def test_mean_distance(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            arr = array(sdm.distance(a))
            value = abs(arr.mean()-sdm.get_dimension()/2.)/arr.std()
            self.assertTrue(value <= 1.5)
        #sdm.free()

    def test_writeread(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            sdm.write(a, a)
            b = sdm.read(a)
            self.assertEqual(a.distance_to(b), 0)
        #sdm.free()

    def test_writereadnear(self, distance=50, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            sdm.write(a, a)
            b = a.copy()
            b.bitrandomswap(distance)
            c = sdm.read(b)
            self.assertEqual(a.distance_to(c), 0)
        #sdm.free()


class MemoryThreadTestCase(unittest.TestCase):

    def setUp(self):
        sdm.initialize()

    def tearDown(self):
        sdm.free()

    def test_distance(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            d1 = sdm.distance(a)
            d2 = sdm.thread_distance(a)
            self.assertEqual(d1, d2)
        #sdm.free()

    def test_radius_count(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            cnt1 = sdm.radius_count(a)
            cnt2 = sdm.thread_radius_count(a)
            self.assertEqual(cnt1, cnt2)
        #sdm.free()

    def test_radius_count_intersect(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            b = Bitstring()
            cnt1 = sdm.thread_radius_count_intersect(a, b)
            cnt2 = sdm.thread_radius_count_intersect(a, b)
            self.assertEqual(cnt1, cnt2)
        #sdm.free()

    def test_writeread1(self, qty=20):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            sdm.thread_write(a, a)
            b = sdm.read(a)
            self.assertEqual(a.distance_to(b), 0)
        #sdm.free()

    def test_writeread2(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            sdm.write(a, a)
            b = sdm.thread_read(a)
            self.assertEqual(a.distance_to(b), 0)
        #sdm.free()

    def test_writeread3(self, qty=10):
        #sdm.initialize()
        for i in range(qty):
            a = Bitstring()
            sdm.thread_write(a, a)
            b = sdm.thread_read(a)
            self.assertEqual(a.distance_to(b), 0)
        #sdm.free()



if __name__ == '__main__':
    sdm.set_dimension(256)
    sdm.set_radius(104)
    unittest.main()

