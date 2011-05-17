import unittest
import pysal
from pysal.core.IOHandlers.stata_txt import StataTextIO
import tempfile
import os

class test_StataTextIO(unittest.TestCase):
    def setUp(self):
        self.test_file_sparse = test_file_sparse = '../../../examples/stata_sparse.txt'
        self.test_file_full = test_file_full = '../../../examples/stata_full.txt'
        self.obj_sparse = StataTextIO(test_file_sparse, 'rs')
        self.obj_full = StataTextIO(test_file_full, 'rs')

    def test_close(self):
        for obj in [self.obj_sparse, self.obj_full]:
            f = obj
            f.close()
            self.failUnlessRaises(ValueError, f.read)

    def test_read(self):
        w_sparse = self.obj_sparse.read()
        self.assertEqual(56, w_sparse.n)
        self.assertEqual(4.0, w_sparse.mean_neighbors)
        self.assertEqual([1.0, 1.0, 1.0, 1.0, 1.0], w_sparse[1].values())

        w_full = self.obj_full.read()
        self.assertEqual(56, w_full.n)
        self.assertEqual(4.0, w_full.mean_neighbors)
        self.assertEqual([0.125, 0.125, 0.125, 0.125, 0.125], w_full[1].values())

    def test_seek(self):
        self.test_read()
        self.failUnlessRaises(StopIteration, self.obj_sparse.read)
        self.failUnlessRaises(StopIteration, self.obj_full.read)
        self.obj_sparse.seek(0)
        self.obj_full.seek(0)
        self.test_read()

    def test_write(self):
        for obj in [self.obj_sparse, self.obj_full]:
            w = obj.read()
            f = tempfile.NamedTemporaryFile(suffix='.txt',dir="../../../examples")
            fname = f.name
            f.close()
            o = pysal.open(fname,'ws')
            o.write(w)
            o.close()
            wnew =  pysal.open(fname,'rs').read()
            self.assertEqual( wnew.pct_nonzero, w.pct_nonzero)
            os.remove(fname)

if __name__ == '__main__':
    unittest.main()