from PySpice.Spice.Netlist import Circuit

class NodeNames:
    """ Allow setting of nodes with appropriate names. """
    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, arg)

 

def cria_amp_op(circuit: Circuit, nome: str, input_pos: str, input_neg: str, Vcc_pos: str, Vcc_neg: str, output: str) -> Circuit:
    """Configura um amp Op com as características do uA741"""
    circuit.include("uA741.lib")
    circuit.X(nome, "uA741", input_pos , input_neg, Vcc_pos, Vcc_neg , output)
    return circuit

def Cria_circuito_eletreto(circuit: Circuit, MicF: float, ResVar: float)-> Circuit:
    n = NodeNames('ArdVIn', 'ArdRecp', 'GNDv','McOut','n1' ,'n2', 'n3', 'n4', 'n5')
    gnd = circuit.gnd
    ## seguidor de tensão pra dividir criar o GndV
    # divisor de tensão 
    circuit.V('in_Ard', n.ArdVIn, gnd, 5)
    circuit.R('1_divTen', n.ArdVIn, n.n1, 1e3)
    circuit.R('2_divTen', n.n1, gnd, 1e3)
    # amp op na configuração de seguidor não inversor
    circuit = cria_amp_op(circuit,".AmpOp_Seg_GNDv", n.n1, n.GNDv, n.ArdVIn, gnd, n.GNDv)
    ## Criando o simulador de microfone com capacitor 
    circuit.C('mic', n.McOut , n.GNDv, MicF)
    circuit.R('1_mic',n.ArdVIn ,n.McOut, 1e3)
    circuit.C('1_passaAlta', n.McOut, n.n2, 1e-6) 
    circuit.R('1_passaAlta', n.n2, n.GNDv, 1e3)
    circuit = cria_amp_op(circuit, '.AmpOp_Seg_PreAmp', n.n2, n.n3, n.ArdVIn, gnd, n.n3)
    circuit.R('1_passaBaixa', n.n3, n.n4, 1e3)
    circuit.C('1_passaBaixa', n.n4, n.GNDv, 1e-6)
    circuit = cria_amp_op(circuit, '.AmpOp_Amp', n.n4, n.n5, n.ArdVIn, gnd, n.ArdRecp)
    circuit.R('b_amp',n.n5, n.GNDv, 1e3)
    circuit.R('f_amp', n.n5, n.ArdRecp, ResVar)
    print(circuit)
    return circuit

circuito = Circuit("circuito_eletreto")
Cria_circuito_eletreto(circuito, 1e-9, 2e3)