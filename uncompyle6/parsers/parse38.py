#  Copyright (c) 2017-2019 Rocky Bernstein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
spark grammar differences over Python 3.7 for Python 3.8
"""
from __future__ import print_function

from uncompyle6.parser import PythonParserSingle
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parsers.parse37 import Python37Parser

class Python38Parser(Python37Parser):
    def p_38walrus(self, args):
        """
        # named_expr is also known as the "walrus op" :=
        expr              ::= named_expr
        named_expr        ::= expr DUP_TOP store
        """

    def p_38misc(self, args):
        """
        stmt               ::= async_for_stmt38
        stmt               ::= async_forelse_stmt38
        stmt               ::= for38
        stmt               ::= forelsestmt38
        stmt               ::= forelselaststmt38
        stmt               ::= forelselaststmtl38
        stmt               ::= tryfinally38stmt
        stmt               ::= tryfinally38rstmt
        stmt               ::= tryfinally38astmt
        stmt               ::= try_elsestmtl38
        stmt               ::= try_except_ret38
        stmt               ::= try_except38
        stmt               ::= whilestmt38
        stmt               ::= whileTruestmt38
        stmt               ::= call
        stmt               ::= ifstmtl

        break ::= POP_BLOCK BREAK_LOOP
        break ::= POP_BLOCK POP_TOP BREAK_LOOP
        break ::= POP_TOP BREAK_LOOP
        break ::= POP_EXCEPT BREAK_LOOP

        # FIXME: this should be restricted to being inside a try block
        stmt               ::= except_ret38

        # FIXME: this should be added only when seeing GET_AITER or YIELD_FROM
        async_for_stmt38   ::= expr
                               GET_AITER
                               SETUP_FINALLY
                               GET_ANEXT
                               LOAD_CONST
                               YIELD_FROM
                               POP_BLOCK
                               store for_block
                               COME_FROM_FINALLY
                               END_ASYNC_FOR

        # FIXME: come froms after the else_suite or END_ASYNC_FOR distinguish which of
        # for / forelse is used. Add come froms and check of add up control-flow detection phase.
        async_forelse_stmt38 ::= expr
                               GET_AITER
                               SETUP_FINALLY
                               GET_ANEXT
                               LOAD_CONST
                               YIELD_FROM
                               POP_BLOCK
                               store for_block
                               COME_FROM_FINALLY
                               END_ASYNC_FOR
                               else_suite


        async_with_stmt    ::= expr BEFORE_ASYNC_WITH GET_AWAITABLE LOAD_CONST YIELD_FROM
                               SETUP_ASYNC_WITH POP_TOP
                               suite_stmts
                               POP_TOP POP_BLOCK
                               BEGIN_FINALLY COME_FROM_ASYNC_WITH
                               WITH_CLEANUP_START
                               GET_AWAITABLE LOAD_CONST YIELD_FROM
                               WITH_CLEANUP_FINISH END_FINALLY

        async_with_as_stmt ::= expr BEFORE_ASYNC_WITH GET_AWAITABLE LOAD_CONST YIELD_FROM
                               SETUP_ASYNC_WITH store
                               suite_stmts
                               POP_TOP POP_BLOCK
                               BEGIN_FINALLY COME_FROM_ASYNC_WITH
                               WITH_CLEANUP_START
                               GET_AWAITABLE LOAD_CONST YIELD_FROM
                               WITH_CLEANUP_FINISH END_FINALLY

        return             ::= ret_expr ROT_TWO POP_TOP RETURN_VALUE

        # 3.8 can push a looping JUMP_BACK into into a JUMP_ from a statement that jumps to it
        lastl_stmt         ::= ifpoplaststmtl
        ifpoplaststmtl     ::= testexpr POP_TOP c_stmts_opt JUMP_BACK
        ifelsestmtl        ::= testexpr c_stmts_opt jb_cfs else_suitel JUMP_BACK come_froms

        _ifstmts_jumpl     ::= c_stmts JUMP_BACK
        _ifstmts_jumpl     ::= _ifstmts_jump
        ifstmtl            ::= testexpr _ifstmts_jumpl

        for38              ::= expr get_iter store for_block JUMP_BACK
        for38              ::= expr get_for_iter store for_block JUMP_BACK
        for38              ::= expr get_for_iter store for_block JUMP_BACK POP_BLOCK
        for38              ::= expr get_for_iter store for_block

        forelsestmt38      ::= expr get_for_iter store for_block POP_BLOCK else_suite
        forelselaststmt38  ::= expr get_for_iter store for_block POP_BLOCK else_suitec
        forelselaststmtl38 ::= expr get_for_iter store for_block POP_BLOCK else_suitel

        whilestmt38        ::= _come_froms testexpr l_stmts_opt COME_FROM JUMP_BACK POP_BLOCK
        whilestmt38        ::= _come_froms testexpr l_stmts_opt JUMP_BACK POP_BLOCK
        whilestmt38        ::= _come_froms testexpr l_stmts_opt JUMP_BACK come_froms
        whilestmt38        ::= _come_froms testexpr returns               POP_BLOCK
        whilestmt38        ::= _come_froms testexpr l_stmts     JUMP_BACK
        whilestmt38        ::= _come_froms testexpr l_stmts     come_froms

        # while1elsestmt   ::=          l_stmts     JUMP_BACK
        whileTruestmt      ::= _come_froms l_stmts              JUMP_BACK POP_BLOCK
        while1stmt         ::= _come_froms l_stmts COME_FROM_LOOP
        while1stmt         ::= _come_froms l_stmts COME_FROM JUMP_BACK COME_FROM_LOOP
        whileTruestmt38    ::= _come_froms l_stmts JUMP_BACK
        whileTruestmt38    ::= _come_froms l_stmts JUMP_BACK COME_FROM_EXCEPT_CLAUSE

        for_block          ::= _come_froms l_stmts_opt _come_from_loops JUMP_BACK

        except_cond1       ::= DUP_TOP expr COMPARE_OP jmp_false
                               POP_TOP POP_TOP POP_TOP
                               POP_EXCEPT

        try_elsestmtl38    ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               except_handler38 COME_FROM
                               else_suitel opt_come_from_except
        try_except         ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               except_handler38
        try_except38       ::= SETUP_FINALLY POP_BLOCK POP_TOP suite_stmts_opt
                               except_handler38a
        try_except_ret38   ::= SETUP_FINALLY expr POP_BLOCK
                               RETURN_VALUE except_ret38a

        # Note: there is a suite_stmts_opt which seems
        # to be bookkeeping which is not expressed in source code
        except_ret38       ::= SETUP_FINALLY expr ROT_FOUR POP_BLOCK POP_EXCEPT
                               CALL_FINALLY RETURN_VALUE COME_FROM
                               COME_FROM_FINALLY
                               suite_stmts_opt END_FINALLY
        except_ret38a      ::= COME_FROM_FINALLY POP_TOP POP_TOP POP_TOP
                               expr ROT_FOUR
                               POP_EXCEPT RETURN_VALUE END_FINALLY

        except_handler38   ::= _jump COME_FROM_FINALLY
                               except_stmts END_FINALLY opt_come_from_except
        except_handler38a  ::= COME_FROM_FINALLY POP_TOP POP_TOP POP_TOP
                               POP_EXCEPT POP_TOP stmts END_FINALLY

        tryfinallystmt     ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               BEGIN_FINALLY COME_FROM_FINALLY suite_stmts_opt
                               END_FINALLY
        tryfinally38rstmt  ::= SETUP_FINALLY POP_BLOCK CALL_FINALLY
                               returns
                               COME_FROM_FINALLY END_FINALLY suite_stmts
        tryfinally38rstmt  ::= SETUP_FINALLY POP_BLOCK CALL_FINALLY
                               returns
                               COME_FROM_FINALLY POP_FINALLY returns
                               END_FINALLY
        tryfinally38stmt   ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               BEGIN_FINALLY COME_FROM_FINALLY
                               POP_FINALLY suite_stmts_opt END_FINALLY
        tryfinally38stmt   ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               BEGIN_FINALLY COME_FROM_FINALLY
                               POP_FINALLY suite_stmts_opt END_FINALLY
        tryfinally38astmt  ::= LOAD_CONST SETUP_FINALLY suite_stmts_opt POP_BLOCK
                               BEGIN_FINALLY COME_FROM_FINALLY
                               POP_FINALLY POP_TOP suite_stmts_opt END_FINALLY POP_TOP
        """

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python38Parser, self).__init__(debug_parser)
        self.customized = {}

    def remove_rules_38(self):
        self.remove_rules(
            """
           stmt               ::= async_for_stmt37
           stmt               ::= for
           stmt               ::= forelsestmt
           stmt               ::= try_except36
           stmt               ::= async_forelse_stmt

           async_for_stmt     ::= setup_loop expr
                                  GET_AITER
                                  SETUP_EXCEPT GET_ANEXT LOAD_CONST
                                  YIELD_FROM
                                  store
                                  POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT DUP_TOP
                                  LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_TRUE
                                  END_FINALLY COME_FROM
                                  for_block
                                  COME_FROM
                                  POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_TOP POP_BLOCK
                                  COME_FROM_LOOP
           async_for_stmt37   ::= setup_loop expr
                                  GET_AITER
                                  SETUP_EXCEPT GET_ANEXT
                                  LOAD_CONST YIELD_FROM
                                  store
                                  POP_BLOCK JUMP_BACK COME_FROM_EXCEPT DUP_TOP
                                  LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_TRUE
                                  END_FINALLY for_block COME_FROM
                                  POP_TOP POP_TOP POP_TOP POP_EXCEPT
                                  POP_TOP POP_BLOCK
                                  COME_FROM_LOOP

          async_forelse_stmt ::= setup_loop expr
                                 GET_AITER
                                 SETUP_EXCEPT GET_ANEXT LOAD_CONST
                                 YIELD_FROM
                                 store
                                 POP_BLOCK JUMP_FORWARD COME_FROM_EXCEPT DUP_TOP
                                 LOAD_GLOBAL COMPARE_OP POP_JUMP_IF_TRUE
                                 END_FINALLY COME_FROM
                                 for_block
                                 COME_FROM
                                 POP_TOP POP_TOP POP_TOP POP_EXCEPT POP_TOP POP_BLOCK
                                 else_suite COME_FROM_LOOP

           for                ::= setup_loop expr get_for_iter store for_block POP_BLOCK
           for                ::= setup_loop expr get_for_iter store for_block POP_BLOCK NOP

           for_block          ::= l_stmts_opt COME_FROM_LOOP JUMP_BACK
           forelsestmt        ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suite
           forelselaststmt    ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suitec
           forelselaststmtl   ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suitel

           tryelsestmtl3      ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                                  except_handler COME_FROM else_suitel
                                  opt_come_from_except
           try_except         ::= SETUP_EXCEPT suite_stmts_opt POP_BLOCK
                                  except_handler opt_come_from_except
           tryfinallystmt     ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                                  LOAD_CONST COME_FROM_FINALLY suite_stmts_opt
                                  END_FINALLY
           tryfinally36       ::= SETUP_FINALLY returns
                                  COME_FROM_FINALLY suite_stmts_opt END_FINALLY
           tryfinally_return_stmt ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                                      LOAD_CONST COME_FROM_FINALLY
        """
        )

    def customize_grammar_rules(self, tokens, customize):
        super(Python37Parser, self).customize_grammar_rules(tokens, customize)
        self.remove_rules_38()
        self.check_reduce["whileTruestmt38"] = "tokens"
        self.check_reduce["whilestmt38"] = "tokens"

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        invalid = super(Python38Parser,
                        self).reduce_is_invalid(rule, ast,
                                                tokens, first, last)
        self.remove_rules_38()
        if invalid:
            return invalid
        lhs = rule[0]
        if lhs in ("whileTruestmt38", "whilestmt38"):
            jb_index = last - 1
            while jb_index > 0 and tokens[jb_index].kind.startswith("COME_FROM"):
                jb_index -= 1
            t = tokens[jb_index]
            if t.kind != "JUMP_BACK":
                return True
            return t.attr != tokens[first].off2int()
            pass

        return False


class Python38ParserSingle(Python38Parser, PythonParserSingle):
    pass


if __name__ == "__main__":
    # Check grammar
    # FIXME: DRY this with other parseXX.py routines
    p = Python38Parser()
    p.remove_rules_38()
    p.check_grammar()
    from uncompyle6 import PYTHON_VERSION, IS_PYPY

    if PYTHON_VERSION == 3.8:
        lhs, rhs, tokens, right_recursive, dup_rhs = p.check_sets()
        from uncompyle6.scanner import get_scanner

        s = get_scanner(PYTHON_VERSION, IS_PYPY)
        opcode_set = set(s.opc.opname).union(
            set(
                """JUMP_BACK CONTINUE RETURN_END_IF COME_FROM
               LOAD_GENEXPR LOAD_ASSERT LOAD_SETCOMP LOAD_DICTCOMP LOAD_CLASSNAME
               LAMBDA_MARKER RETURN_LAST
            """.split()
            )
        )
        remain_tokens = set(tokens) - opcode_set
        import re

        remain_tokens = set([re.sub(r"_\d+$", "", t) for t in remain_tokens])
        remain_tokens = set([re.sub("_CONT$", "", t) for t in remain_tokens])
        remain_tokens = set(remain_tokens) - opcode_set
        print(remain_tokens)
        import sys
        if len(sys.argv) > 1:
            from spark_parser.spark import rule2str
            for rule in sorted(p.rule2name.items()):
                print(rule2str(rule[0]))
