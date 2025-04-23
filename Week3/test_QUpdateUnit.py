from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim
from QUpdateUnit import QUpdateUnit

def test_q_update_unit():
    run_test_vector_sim( QUpdateUnit(), [
      # q_sa    max_q_sp  reward   alpha   gamma   q_sa_new
      [ 0x0000, 0x0000,   0xFFF0,  0x0008,  0x000E, 0xF800 ],  # expect -2048
      [ 0x0800, 0x0800,   0x0004,  0x0008,  0x000E, 0x0802 ],  # sample case
    ], cmdline_opts=None )
