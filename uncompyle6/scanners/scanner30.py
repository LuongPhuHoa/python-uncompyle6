#  Copyright (c) 2016 by Rocky Bernstein
"""
Python 3.0 bytecode scanner/deparser

This sets up opcodes Python's 3.0 and calls a generalized
scanner routine for Python 3.
"""

# bytecode verification, verify(), uses JUMP_OPs from here
from xdis.opcodes import opcode_30 as opc
JUMP_OPs = map(lambda op: opc.opname[op], opc.hasjrel + opc.hasjabs)

from uncompyle6.scanners.scanner3 import Scanner3
class Scanner30(Scanner3):

    def __init__(self, show_asm=None, is_pypy=False):
        Scanner3.__init__(self, 3.0, show_asm, is_pypy)
        return
    pass

if __name__ == "__main__":
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 3.0:
        import inspect
        co = inspect.currentframe().f_code
        tokens, customize = Scanner30().ingest(co)
        for t in tokens:
            print(t)
        pass
    else:
        print("Need to be Python 3.0 to demo; I am %s." %
              PYTHON_VERSION)