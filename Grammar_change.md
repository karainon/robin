single_input: NEWLINE | simple_stmt | compound_stmt NEWLINE
file_input: (NEWLINE | stmt)* ENDMARKER
stmt: simple_stmt | compound_stmt


    simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
        small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt | assert_stmt)
            expr_stmt: testlist_star_expr (annassign | augassign (yield_expr|testlist) | ('=' (yield_expr|testlist_star_expr))*)
                testlist_star_expr: (test|star_expr) (',' (test|star_expr))* [',']
                annassign: ':' test ['=' test]
                augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//=')
                yield_expr: 'yield' [yield_arg]
                    yield_arg: 'from' test | testlist
            del_stmt: 'del' exprlist
            pass_stmt: 'pass'
            flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt
                break_stmt: 'break'
                continue_stmt: 'continue'
                return_stmt: 'return' [testlist]
                raise_stmt: 'raise' [test ['from' test]]
                yield_stmt: yield_expr
            import_stmt: import_name | import_from
                import_name: 'import' dotted_as_names
                    dotted_as_names: dotted_as_name (',' dotted_as_name)*
                        dotted_as_name: dotted_name ['as' NAME]

                import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+) 'import' ('*' | '(' import_as_names ')' | import_as_names))
                    dotted_name: NAME ('.' NAME)*
                    import_as_names: import_as_name (',' import_as_name)* [',']
                        import_as_name: NAME ['as' NAME]

            global_stmt: 'global' NAME (',' NAME)*
            nonlocal_stmt: 'nonlocal' NAME (',' NAME)*
            assert_stmt: 'assert' test [',' test]


    compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt
        if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ['else' ':' suite]
            suite: simple_stmt | NEWLINE INDENT (simple_stmt | compound_stmt)+ DEDENT
            >>>>>>
            test: or_test ['if' or_test 'else' test] | lambdef
                or_test: and_test ('or' and_test)*
                    and_test: not_test ('and' not_test)*
                        not_test: 'not' not_test | comparison
                            comparison: expr (comp_op expr)*
                                comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'

                lambdef: 'lambda' [varargslist] ':' test

            <<<<<<
                    >>>>>>
                    varargslist: (vfpdef   ['=' test]   (',' vfpdef ['=' test])*
                                    [',' [    '*' [vfpdef]  (',' vfpdef ['=' test])*  [',' ['**' vfpdef [',']]] | '**' vfpdef [',']   ]]
                                    | '*' [vfpdef] (',' vfpdef ['=' test])* [',' ['**' vfpdef [',']]]
                                    | '**' vfpdef [',']
                                 )
                        vfpdef: NAME
                    <<<<<<


        while_stmt: 'while' test ':' suite ['else' ':' suite]
        for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
            testlist: test (',' test)* [',']
            exprlist: (expr|star_expr) (',' (expr|star_expr))* [',']
                star_expr: '*' expr

                >>>>>
                expr: xor_expr ('|' xor_expr)*
                    xor_expr: and_expr ('^' and_expr)*
                        and_expr: shift_expr ('&' shift_expr)*
                            shift_expr: arith_expr (('<<'|'>>') arith_expr)*
                                arith_expr: term (('+'|'-') term)*
                                    term: factor (('*'|'@'|'/'|'%'|'//') factor)*
                                        factor: ('+'|'-'|'~') factor | power
                                            power: atom_expr ['**' factor]
                                                atom_expr: [AWAIT] atom trailer*
                <<<<<

                                                    atom: ('(' [yield_expr|testlist_comp] ')' |
                                                           '[' [testlist_comp] ']' |
                                                           '{' [dictorsetmaker] '}' |
                                                           NAME | NUMBER | STRING+ | '...' | 'None' | 'True' | 'False')
                                                        testlist_comp: (test|star_expr) ( comp_for | (',' (test|star_expr))* [','] )
                                                        dictorsetmaker: ( ((test ':' test | '**' expr)
                                                                           (comp_for | (',' (test ':' test | '**' expr))* [','])) |
                                                                          ((test | star_expr)
                                                                           (comp_for | (',' (test | star_expr))* [','])) )

                                                    trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
                                                        subscriptlist: subscript (',' subscript)* [',']
                                                            subscript: test | [test] ':' [test] [sliceop]
                                                                sliceop: ':' [test]



        try_stmt: ('try' ':' suite ((except_clause ':' suite) + ['else' ':' suite] ['finally' ':' suite] | 'finally' ':' suite))
            except_clause: 'except' [test ['as' NAME]]

        with_stmt: 'with' with_item (',' with_item)*  ':' suite
            with_item: test ['as' expr]

        funcdef: 'def' NAME parameters ['->' test] ':' suite
            parameters: '(' [typedargslist] ')'

                >>>>>>
                typedargslist: (tfpdef ['=' test] (',' tfpdef ['=' test])* [',' [ '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]] | '**' tfpdef [',']]]
                                | '*' [tfpdef] (',' tfpdef ['=' test])* [',' ['**' tfpdef [',']]]
                                | '**' tfpdef [',']
                               )
                    tfpdef: NAME [':' test]
                <<<<<<

        classdef: 'class' NAME ['(' [arglist] ')'] ':' suite
            arglist: argument (',' argument)*  [',']
                argument: ( test [comp_for] | test '=' test | '**' test | '*' test )
                    comp_for: [ASYNC] 'for' exprlist 'in' or_test [comp_iter]
                        comp_iter: comp_for | comp_if
                            comp_if: 'if' test_nocond [comp_iter]
                                test_nocond: or_test | lambdef_nocond
                                    lambdef_nocond: 'lambda' [varargslist] ':' test_nocond

        decorated: decorators (classdef | funcdef | async_funcdef)
            decorators: decorator+
                decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
            async_funcdef: ASYNC funcdef
        async_stmt: ASYNC (funcdef | with_stmt | for_stmt)


encoding_decl: NAME


