from pymtl3 import *

class QUpdateUnit(Component):
    def construct(s):
        DATA_WIDTH = 16

        # Ports
        s.q_sa       = InPort ( Bits16 )
        s.max_q_sp   = InPort ( Bits16 )
        s.reward     = InPort ( Bits16 )
        s.alpha      = InPort ( Bits16 )
        s.gamma      = InPort ( Bits16 )
        s.q_sa_new   = OutPort( Bits16 )

        # Intermediate wires
        s.discounted_q = Wire( Bits16 )
        s.target       = Wire( Bits16 )
        s.q1           = Wire( Bits16 )
        s.q2           = Wire( Bits16 )

        # RTL logic
        @update
        def comb_logic():
            s.discounted_q @= sext((s.gamma * s.max_q_sp) >> 4, 16)
            s.target       @= s.reward + s.discounted_q
            s.q1           @= sext(((16 - s.alpha) * s.q_sa) >> 4, 16)
            s.q2           @= sext((s.alpha * s.target) >> 4, 16)
            s.q_sa_new     @= s.q1 + s.q2
