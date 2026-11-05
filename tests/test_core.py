"""Quick checks of the core steps on synthetic point clouds: no datasets and no GPU needed.

    MFLPR_DEVICE=cpu python -m unittest discover -s tests -v      (from the repository root)
"""
import os
import sys
import unittest

import numpy as np

os.environ.setdefault('MFLPR_DEVICE', 'cpu')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import helper  # noqa: E402


def make_lpr(map_res=0.5, dim=120, block=2, background=0.0):
    """A LiDAR_PlaceRec with only the parameters the descriptor and matching steps read (no dataset loading)."""
    lpr = helper.LiDAR_PlaceRec.__new__(helper.LiDAR_PlaceRec)
    lpr.mapRes, lpr.blockSize = map_res, block
    lpr.scanDimX = lpr.scanDimY = dim // block
    lpr.HDMThresh, lpr.background, lpr.n = 1, background, 1
    lpr.randDwnsmple_nMult, lpr.randDwnsmple_dim, lpr.configParams = 0, 10, {}
    return lpr


def synthetic_scene(seed=0):
    """Walls and poles around the origin, as a LiDAR on a vehicle would see them."""
    rng = np.random.default_rng(seed)
    pts = []
    for _ in range(25):
        x0, y0 = rng.uniform(-25, 25, 2)
        ang, length = rng.uniform(0, np.pi), rng.uniform(2, 12)
        s = rng.uniform(0, length, 200)
        pts.append(np.c_[x0 + s * np.cos(ang), y0 + s * np.sin(ang), rng.uniform(0.2, 3, 200)])
    for x0, y0 in rng.uniform(-25, 25, (15, 2)):
        pts.append(np.c_[x0 + rng.normal(0, 0.05, 60), y0 + rng.normal(0, 0.05, 60), rng.uniform(0.2, 4, 60)])
    return np.concatenate(pts)


class CoreSteps(unittest.TestCase):
    def test_rotation_round_trip(self):
        lpr = make_lpr()
        x, y = np.array([1.0, -2.0, 3.5]), np.array([0.5, 4.0, -1.0])
        xr, yr = lpr.applyingRotation2D(37, x, y)
        xb, yb = lpr.applyingRotation2D(-37, xr, yr)
        np.testing.assert_allclose(np.c_[xb, yb], np.c_[x, y], atol=1e-12)

    def test_descriptor_is_binary_and_sized(self):
        lpr = make_lpr()
        grid = lpr.processing2DScan('REF', synthetic_scene(), sameProcess=True)
        self.assertEqual(grid.shape, (120, 120))
        self.assertTrue(set(np.unique(grid)) <= {0.0, 1.0})
        self.assertGreater(grid.sum(), 100)

    def test_downsampling_caps_each_block(self):
        rng = np.random.default_rng(1)
        grid = (rng.random((40, 40)) < 0.6).astype(int)
        for kind in ('random', 'ordered'):
            out = helper.random_downsample(grid, 10, 2, kind)[:40, :40]
            per_block = out.reshape(4, 10, 4, 10).sum(axis=(1, 3))
            self.assertTrue((per_block <= 20).all(), kind)
            self.assertTrue(((out == 1) <= (grid == 1)).all(), f'{kind} kept a cell that was empty')

    def test_matched_filter_recovers_a_translation(self):
        lpr = make_lpr(map_res=0.5)
        scene = synthetic_scene()
        ref = lpr.processing2DScan('REF', scene, sameProcess=True)
        for shift in ((3.0, -2.0), (-4.5, 1.5)):
            moved = scene - np.r_[shift, 0.0]  # the sensor moved by `shift`, so the scene appears shifted back
            query = lpr.processing2DScan('QUERY', moved, sameProcess=True)
            max_y, max_x = lpr.scanMatchWithConvolution(helper.cp.asarray(ref), 0, rotQuery=query, globalSearch=False)[:2]
            dx, dy = (int(max_x) - ref.shape[1] // 2) * lpr.mapRes, (int(max_y) - ref.shape[0] // 2) * lpr.mapRes
            with self.subTest(shift=shift):
                self.assertAlmostEqual(dx, shift[0], delta=lpr.mapRes)
                self.assertAlmostEqual(dy, shift[1], delta=lpr.mapRes)


if __name__ == '__main__':
    unittest.main(verbosity=2)
