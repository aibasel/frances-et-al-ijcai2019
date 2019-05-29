import os

SRC_ROOT = os.path.dirname(os.path.realpath(__file__))
PKG_ROOT = os.path.dirname(os.path.dirname(SRC_ROOT))

PYPERPLAN_DIR = os.path.join(PKG_ROOT, os.path.join("src", "pyperplan"))

BENCHMARK_DIR = os.path.join(PKG_ROOT, 'benchmarks')

EXPDATA_DIR = os.path.join(PKG_ROOT, 'runs')
