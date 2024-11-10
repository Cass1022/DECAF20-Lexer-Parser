from final_lexer import tokens
import ply.yacc as yacc

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LEQ', 'GEQ', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NOT'),
    ('right', 'ELSE'),
    ('right', 'RPAREN'),
)


def p_Program(p):
    '''Program : Externs PACKAGE ID LCB FieldDecls MethodDecls RCB'''
    p[0] = ('Program', p[1], p[3], p[5], p[6])


def p_Externs(p):
    '''Externs : ExternDefn Externs
                | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_ExternDefn(p):
    '''ExternDefn : EXTERN FUNC ID LPAREN ExternTypeList RPAREN MethodType SEMICOLON'''
    p[0] = ('ExternDefn', p[3], p[5], p[7])


def p_ExternTypeList(p):
    '''ExternTypeList : ExternType
                      | ExternTypeList COMMA ExternType'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_FieldDecls(p):
    '''FieldDecls : FieldDecl FieldDecls
                | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_FieldDecl(p):
    '''FieldDecl : VAR IdTypeList Type SEMICOLON
                 | VAR IdTypeList ArrayType SEMICOLON
                 | VAR ID Type ASSIGN Constant SEMICOLON'''
    if len(p) == 5:
        p[0] = [('var_decl', var, p[3]) for var in p[2]]
    elif len(p) == 6:
        p[0] = ('var_constant', p[2], p[3], p[5])


def p_MethodDecls(p):
    '''MethodDecls : MethodDecl MethodDecls
                    | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_MethodDecl(p):
    '''MethodDecl : FUNC ID LPAREN ParamList RPAREN MethodType Block
                  | FUNC ID LPAREN RPAREN MethodType Block'''
    if len(p) == 8:
        p[0] = (p[1], p[2], p[4], p[6], p[7])
    else:
        p[0] = (p[1], p[2], [], p[5], p[6])


def p_Block(p):
    '''Block : LCB VarDecls Statements RCB'''
    p[0] = ('block', p[2], p[3])


def p_VarDecls(p):
    '''VarDecls : VarDecl VarDecls
                | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_VarDecl(p):
    '''VarDecl : VAR IdTypeList Type SEMICOLON'''
    p[0] = ('var_decl', p[2], p[3])


def p_IdTypeList(p):
    '''IdTypeList : ID
                | ID COMMA IdTypeList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_ParamList(p):
    '''ParamList : ID Type
                 | ID Type COMMA ParamList'''
    if len(p) == 3:
        p[0] = [('param', p[1], p[2])]
    else:
        p[0] = [('param', p[1], p[2])] + p[4]


def p_Statements(p):
    '''Statements : Statement Statements
                    | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_Statement(p):
    '''Statement : Block
                | Assign SEMICOLON
                | MethodCall SEMICOLON
                | IF LPAREN Expr RPAREN Block
                | IF LPAREN Expr RPAREN Block ELSE Block
                | WHILE LPAREN Expr RPAREN Block
                | FOR LPAREN AssignList SEMICOLON Expr SEMICOLON AssignList RPAREN Block
                | RETURN SEMICOLON
                | RETURN LPAREN RPAREN SEMICOLON
                | RETURN LPAREN Expr RPAREN SEMICOLON
                | BREAK SEMICOLON
                | CONTINUE SEMICOLON'''
    # Block statement
    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        p[0] = ('assign_stmt', p[1])

    # If-else without else
    elif len(p) == 6:
        p[0] = ('if_stmt', p[3], p[5])

    # If-else with else
    elif len(p) == 8:
        p[0] = ('if_else_stmt', p[3], p[5], p[7])

    elif len(p) == 6 and p[1] == 'while':
        p[0] = ('while_stmt', p[3], p[5])

    elif len(p) == 10 and p[1] == 'for':
        p[0] = ('for_stmt', p[3], p[5], p[7], p[9])

    # Return without a value
    elif len(p) == 3 and p[1] == 'return':
        p[0] = ('return_stmt', None)

    # Return with empty parentheses
    elif len(p) == 5 and p[3] == ')':
        p[0] = ('return_stmt', None)

    # Return with expression
    elif len(p) == 5:
        p[0] = ('return_stmt', p[3])

    elif p[1] == 'break':
        p[0] = ('break_stmt',)

    elif p[1] == 'continue':
        p[0] = ('continue_stmt',)


def p_AssignList(p):
    '''AssignList : Assign
                    | Assign COMMA AssignList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_Assign(p):
    '''Assign : Lvalue ASSIGN Expr'''
    p[0] = ('assign', p[1], p[3])


def p_Lvalue(p):
    '''Lvalue : ID
            | ID LSB Expr RCB'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('Lvalue', p[1], p[3])


def p_MethodCall(p):
    '''MethodCall : ID LPAREN RPAREN
                | ID LPAREN MethodArgList RPAREN'''
    if len(p) == 4:
        p[0] = ('MethodCall', p[1], [])
    else:
        p[0] = ('MethodCall', p[1], p[3])


def p_MethodArgList(p):
    '''MethodArgList : MethodArg
                    | MethodArg COMMA MethodArgList'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_MethodArg(p):
    '''MethodArg : Expr
                | STRINGCONSTANT'''
    p[0] = p[1]


def p_Expr(p):
    '''Expr : ID
            | MethodCall
            | Constant
            | Expr BinaryOperator Expr
            | UnaryOperator Expr
            | LPAREN Expr RPAREN
            | ID LSB Expr RSB'''

    # ID
    if len(p) == 2:
        p[0] = ('id', p[1])

    # BinaryOperator
    elif len(p) == 4 and p[2] != '[':
        p[0] = ('binary_op', p[2], p[1], p[3])

    # LPAREN Expr RPAREN
    elif len(p) == 4 and p[2] == '(':
        p[0] = p[2]

    # UnaryOperator
    elif len(p) == 3:
        p[0] = ('unary_op', p[1], p[2])

    # Array indexing
    elif len(p) == 5:
        p[0] = ('array', p[1], p[3])

    # MethodCall, Constant
    else:
        p[0] = p[1]


def p_UnaryOperator(p):
    '''UnaryOperator : UnaryNot
                    | UnaryMinus'''
    p[0] = p[1]


def p_UnaryNot(p):
    '''UnaryNot : NOT'''
    p[0] = p[1]


def p_UnaryMinus(p):
    '''UnaryMinus : MINUS'''
    p[0] = p[1]


def p_BinaryOperator(p):
    '''BinaryOperator : ArithmeticOperator
                    | BooleanOperator'''

    p[0] = p[1]


def p_ArithmeticOperator(p):
    '''ArithmeticOperator : PLUS
                        | MINUS
                        | MULT
                        | DIV
                        | LEFTSHIFT
                        | RIGHTSHIFT
                        | MOD'''
    p[0] = p[1]


def p_BooleanOperator(p):
    '''BooleanOperator : EQ
                        | NEQ
                        | LT
                        | LEQ
                        | GT
                        | GEQ
                        | AND
                        | OR'''
    p[0] = p[1]


def p_ExternType(p):
    '''ExternType : STRINGTYPE
                    | Type'''
    p[0] = p[1]


def p_Type(p):
    '''Type : INTTYPE
            | BOOLTYPE'''
    p[0] = p[1]


def p_MethodType(p):
    '''MethodType : VOID
                | Type'''
    p[0] = p[1]


def p_BoolConstant(p):
    '''BoolConstant : TRUE
                    | FALSE'''
    p[0] = p[1]


def p_ArrayType(p):
    '''ArrayType : LSB INTCONSTANT RSB Type'''
    p[0] = p[2] + p[4]


def p_Constant(p):
    '''Constant : INTCONSTANT
                | CHARCONSTANT
                | BoolConstant'''
    p[0] = p[1]


def p_empty(p):
    '''empty : '''
    pass


def p_error(p):
    if p:
        line_number = p.lineno
        lexpos = p.lexpos

        # Get the line of code where the error occurred
        line = p.lexer.lexdata.splitlines()[line_number - 1]

        # Calculate column (position within the line)
        column = lexpos - p.lexer.lexdata.rfind('\n', 0, lexpos)

        print(f"*** Error line {line_number}.")
        print(line)
        print(" " * (column - 1) + "^")
        print(f"*** syntax error at {p.type}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()
filename = 'test.decaf'

with open(filename, 'r') as file:
    data = file.read()
    result = parser.parse(data)
    print(result)
