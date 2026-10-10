"""unittest wrapper so the Vibe watchdog recognises gate runs: python3 -m unittest tests.test_site.Seg2"""
import subprocess, sys, os, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
def run(mode):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'check_site.py'), mode], capture_output=True, text=True)
    return r.returncode, r.stdout
def make(mode):
    class T(unittest.TestCase):
        def test_gate(self):
            code, out = run(mode)
            self.assertEqual(code, 0, out)
    T.__name__ = mode.capitalize(); return T
Ds, Seg1, Seg2, Seg3, Seg4 = (make(m) for m in ('ds', 'seg1', 'seg2', 'seg3', 'seg4'))
