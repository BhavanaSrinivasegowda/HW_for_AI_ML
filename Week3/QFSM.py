# QLearningFSM.py
from pymtl3 import *
from QUpdateUnit import QUpdateUnit
from pymtl3.stdlib.basic_rtl import RegRst

class QFSM(Component):
    def construct(s):
        # Parameters
        BOARD_SIZE = 5
        ACTIONS = 4
        DATA_WIDTH = 16

        # Q-table storage
        s.Q_table = [ [ [ Wire( Bits16 ) for _ in range(ACTIONS) ] for _ in range(BOARD_SIZE) ] for _ in range(BOARD_SIZE) ]

        # State & control
        s.s_i = Wire(Bits5)
        s.s_j = Wire(Bits5)
        s.a   = Wire(Bits2)

        s.s_prime_i = Wire(Bits5)
        s.s_prime_j = Wire(Bits5)

        s.reward     = Wire(Bits16)
        s.q_sa       = Wire(Bits16)
        s.q_max_sp   = Wire(Bits16)

        # Connect to QUpdateUnit
        s.q_unit = QUpdateUnit()
        s.q_unit.q_sa     //= s.q_sa
        s.q_unit.max_q_sp //= s.q_max_sp
        s.q_unit.reward   //= s.reward
        s.q_unit.alpha    //= Bits16(8)     # 0.5
        s.q_unit.gamma    //= Bits16(14)    # 0.875

        # FSM
        s.state = RegRst( Bits3, reset_value=0 )

        @update
        def comb_logic():
            # Default state
            s.q_sa     @= s.Q_table[s.s_i][s.s_j][s.a]
            s.q_max_sp @= max([ s.Q_table[s.s_prime_i][s.s_prime_j][k] for k in range(ACTIONS) ])
            s.reward   @= Bits16(-1)

        @update_ff
        def fsm_logic():
            if s.state.out == 0:
                # Initialization state
                s.s_i       <<= 2
                s.s_j       <<= 2
                s.s_prime_i <<= 3
                s.s_prime_j <<= 2
                s.a         <<= 1
                s.state.in_ <<= 1

            elif s.state.out == 1:
                # Wait for update (assume one-cycle delay)
                s.state.in_ <<= 2

            elif s.state.out == 2:
                # Write updated Q value
                s.Q_table[s.s_i][s.s_j][s.a] <<= s.q_unit.q_sa_new
                s.state.in_ <<= 0  # Loop or finish

    def line_trace(s):
        return f"Q_new={s.q_unit.q_sa_new}"
