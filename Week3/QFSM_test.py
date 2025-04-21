from pymtl3 import *
from pymtl3.stdlib.test_utils import run_sim
from QFSM import QFSM

def test_q_learning_fsm():
    dut = QFSM()
    dut.apply( DefaultPassGroup() )
    dut.sim_reset()

    print("\n[INFO] Simulating FSM-driven Q update...")
    for cycle in range(6):
        dut.sim_tick()
        print(dut.line_trace())

if __name__ == '__main__':
    test_q_learning_fsm()
