# untitest_cp.py
# For testing purposes.
# Martin Borgén
# 2023-06-03

import unittest
import time
import Critical_Path
import csv_module

class Test1(unittest.TestCase):

    def setUp(self) -> None:
        self.testData1 = csv_module.csv_reader("test.csv")
        self.testTree1 = Critical_Path.TaskTree()

        for line in self.testData1:
            self.testTree1.createTask(line[0], line[2:], line[1])
        self.starttT = time.time()

    def tearDown(self) -> None:
        t = time.time() - self.starttT
        print(f"Dur: {t} seconds")

    def test_hk_unmod(self):
        self.testTree1.compute()
        self.assertEqual(self.testTree1.criticalPaths[0].totTime, 86)    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test1)
    unittest.TextTestRunner(verbosity=0).run(suite)