"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Abril 15 2023
    Compilador para lenguaje al estilo R/C++.

    CR++, El Cristiano Ronaldo de los Lenguajes de Programación.
"""

# ======================== Sintáxis ======================== #

from Semantics import Rules
from Quadruples import quadsConstructor

rules = Rules()

# ╭──────────────────────────────────────────────────────────────╮
# │                           PROGRAM                            │
# ╰──────────────────────────────────────────────────────────────╯

def p_program(p):
    '''program : block'''
    p[0] = "COMPILED"
    rules.p_end_program()
    quadsConstructor.startCompiler()


def p_block(p):
    '''block : statement block
             | empty'''
                
                
# ╭───────────────────────────╮
# │         Statements        │
# ╰───────────────────────────╯

def p_statement(p):
    '''statement : vars
                 | function
                 | assignment_block
                 | expression
                 | function_call
                 | loop
                 | condition
                 | writing
                 | sort
                 | return
                 | empty'''
    # ! rules.p_saveToOpStack(p) # ! Might be useless, who knows


# ╭───────────────────────────╮
# │            Vars           │
# ╰───────────────────────────╯

def p_vars(p):
    '''vars : type id vars_equals semicolon
            | type id leftbracket var_ctei rightbracket vars_equals semicolon
            | type id leftbracket var_ctei rightbracket leftbracket var_ctei rightbracket vars_equals semicolon'''

            
def p_extra_vars(p):
    '''extra_vars : extra_var_comma id vars_equals
                  | empty'''
    
    
def p_extra_var_comma(p):
    '''extra_var_comma : COMMA'''
    rules.p_updateSymbolTable()
                
                
def p_vars_equals_array(p):
    '''vars_equals_array : leftcorch expression array_vars rightcorch
                         | leftcorch empty rightcorch'''


def p_array_vars(p):
    '''array_vars : comma expression array_vars
                  | empty'''
                
                
def p_vars_equals(p):
    '''vars_equals : assignment vars_equals_array extra_vars
                   | assignment expression extra_vars
                   | extra_vars
                   | empty'''


def p_assignment(p):
    '''assignment : equals
                  | assignl'''
                 
                 
def p_assignl(p):
    '''assignl : ASSIGNL'''
    
    
def p_equals(p):
    '''equals : EQUALS'''


def p_type(p):
    '''type : INT
            | FLOAT
            | BOOL
            | STRING
            | CHAR
            | VOID'''
    rules.p_insertType(p)


def p_id(p):
    '''id : ID'''
    rules.p_insertID(p)


def p_comma(p):
    '''comma : COMMA'''

                
def p_leftcorch(p):
    '''leftcorch : LEFTCORCH'''
    
    
def p_rightcorch(p):
    '''rightcorch : RIGHTCORCH'''
    
    
def p_leftbracket(p):
    '''leftbracket : LEFTBRACKET'''
    

def p_rightbracket(p):
    '''rightbracket : RIGHTBRACKET'''
    
    
def p_semicolon(p):
    '''semicolon : SEMICOLON'''
    rules.p_updateSymbolTable()


# ╭───────────────────────────╮
# │        Expressions        │
# ╰───────────────────────────╯

def p_expression(p):
    '''expression : exp comparation'''
    quadsConstructor.verifyConditionals() # If POper.top == '<' or '>' ...


def p_exp(p):
    '''exp : term operator'''
    quadsConstructor.verifySignPlusOrMinus() # If POper.top == '+' or '-' ...


def p_term(p):
    '''term : fact term_operator'''
    quadsConstructor.verifySignTimesOrDivide()


def p_fact(p):
    '''fact : leftparen expression rightparen
            | media
            | moda
            | mediana
            | var_cte'''


def p_leftparen(p):
    '''leftparen : LEFTPAREN'''


def p_rightparen(p):
    '''rightparen : RIGHTPAREN'''

    
def p_term_operator(p):
    '''term_operator : exponential fact term_operator
                     | times fact term_operator
                     | divide fact term_operator
                     | modulus fact term_operator
                     | empty'''

def p_exponential(p):
    '''exponential : EXPONENTIAL'''
    quadsConstructor.insertSign(p[1])


def p_times(p):
    '''times : TIMES'''
    quadsConstructor.insertSign(p[1])
    
    
def p_divide(p):
    '''divide : DIVIDE'''
    quadsConstructor.insertSign(p[1])
    
    
def p_modulus(p):
    '''modulus : MODULUS'''
    quadsConstructor.insertSign(p[1])


# ╭───────────────────────────╮
# │         Vars CTE          │
# ╰───────────────────────────╯

def p_var_cte(p):
    '''var_cte : var_ctei
               | var_ctef
               | var_string
               | var_id'''
               
               
def p_var_id(p):
    '''var_id : ID'''
    rules.p_saveValue(p)
    quadsConstructor.insertTypeAndID(p[1]) # Nuestro lexer lidia con los números
               
               
def p_var_ctei(p):
    '''var_ctei : CTEI'''
    rules.p_saveValue(p)
    
    
def p_var_ctef(p):
    '''var_ctef : CTEF'''
    rules.p_saveValue(p)
    
    
def p_var_string(p):
    '''var_string : CTESTRING'''
    rules.p_saveValue(p)


# ╭───────────────────────────╮
# │       Comparators         │
# ╰───────────────────────────╯

def p_comparation(p):
    '''comparation : and exp
                   | or exp
                   | greater exp
                   | less exp
                   | notequal exp
                   | notequalnum exp
                   | empty'''


def p_and(p):
    '''and : AND'''
    quadsConstructor.insertSign(p[1])

    
def p_or(p):
    '''or : OR'''
    quadsConstructor.insertSign(p[1])


def p_greater(p):
    '''greater : GREATER'''
    quadsConstructor.insertSign(p[1])


def p_less(p):
    '''less : LESS'''
    quadsConstructor.insertSign(p[1])


def p_notequal(p):
    '''notequal : NOTEQUAL'''
    quadsConstructor.insertSign(p[1])


def p_notequalnum(p):
    '''notequalnum : NOTEQUALNUM'''
    quadsConstructor.insertSign(p[1])


# ╭───────────────────────────╮
# │        Operators          │
# ╰───────────────────────────╯

def p_operator(p):
    '''operator : plus term operator
                | minus term operator
                | empty'''
    # ! quadsConstructor.verifySignPlusOrMinus() ## ! CREO ESTO ARREGLA EXPRESIONES LINEALES O ROMPE MAS


def p_plus(p):
    '''plus : PLUS'''
    quadsConstructor.insertSign(p[1])


def p_minus(p):
    '''minus : MINUS'''
    quadsConstructor.insertSign(p[1])


# ╭───────────────────────────╮
# │         Functions         │
# ╰───────────────────────────╯

def p_function(p):
    '''function : type function_id leftparen function_local_variables
                | empty'''

    
def p_function_id(p):
    '''function_id : ID'''
    rules.p_insertID(p)
    rules.p_isFunction()
    rules.p_insertFunction()
    
    
def p_function_local_variables(p):
    '''function_local_variables : function_parameters nodoregistervars rightparen leftcorch function_block'''
    
    
def p_nodoregistervars(p):
    '''nodoregistervars : empty'''
    rules.p_registerLocalVariables()
    
    
def p_function_block(p):
    '''function_block : block rightcorch'''
    rules.p_insertScope('global')
    rules.parentFunction = None


def p_function_parameters(p):
    '''function_parameters : function_param function_extra_parameters
                           | empty'''
    # ! rules.p_registerLocalVariables() # ! BORRAR CREO
       
                
def p_function_param(p):
    '''function_param : type id'''
    rules.p_insertScope('local')
    rules.p_saveLocalVariable()


def p_function_extra_parameters(p):
    '''function_extra_parameters : function_extra_parameters_comma function_parameters
                                 | empty'''
    rules.p_updateSymbolTable()
                
                
def p_function_extra_parameters_comma(p):
    '''function_extra_parameters_comma : COMMA'''
    rules.p_updateSymbolTable()


def p_assignment_block(p):
    '''assignment_block : ID ASSIGNL expression SEMICOLON
                        | ID EQUALS expression SEMICOLON'''
    rules.values = []  # Por usar una regla compartida (expression), debemos limpiar esto
    quadsConstructor.insertAssignmentID(p[1])
    quadsConstructor.insertAssignmentSign(p[2])
    quadsConstructor.verifyAssignment()


def p_function_call(p):
    '''function_call : id leftparen expression function_call_expressions rightparen'''


def p_function_call_expressions(p):
    '''function_call_expressions : comma function_call_expressions
                                 | empty'''


# ╭───────────────────────────╮
# │           Loops           │
# ╰───────────────────────────╯

def p_loop(p):
    '''loop : nodowhile1 LEFTPAREN expression nodowhile2 leftcorch block rightcorch
            | empty'''
    quadsConstructor.nodoWhileTres()


def p_nodowhile1(p):
    '''nodowhile1 : WHILE'''
    quadsConstructor.nodoWhileUno()


def p_nodowhile2(p):
    '''nodowhile2 : RIGHTPAREN'''
    quadsConstructor.nodoWhileDos()


# ╭───────────────────────────╮
# │         If / Else         │
# ╰───────────────────────────╯

def p_condition(p):
    '''condition : IF LEFTPAREN expression nodocond LEFTCORCH block RIGHTCORCH else_condition'''
    quadsConstructor.nodoCondicionalDos()

def p_nodocond(p):
    '''nodocond : RIGHTPAREN'''
    quadsConstructor.nodoCondicionalUno()


def p_else_condition(p):
    '''else_condition : else LEFTCORCH block RIGHTCORCH
                      | empty'''

def p_else(p):
    '''else : ELSE'''
    quadsConstructor.nodoCondicionalTres()


# ╭───────────────────────────╮
# │           Print           │
# ╰───────────────────────────╯

def p_writing(p):
    '''writing : writingprint LEFTPAREN print_val RIGHTPAREN SEMICOLON'''
    quadsConstructor.verifyPrint()


def p_writingprint(p):
    '''writingprint : PRINT'''
    quadsConstructor.insertPrint(p[1])


def p_print_val(p):
    '''print_val : expression print_exp'''
    # ! if p[1] != None : quadsConstructor.insertPrintString(p[1])


def p_print_exp(p):
    '''print_exp : COMMA print_val
                 | empty'''
                 
                 
# ╭───────────────────────────╮
# │          Extras           │
# ╰───────────────────────────╯

def p_sort(p):
    '''sort : ID PERIOD SORT LEFTPAREN RIGHTPAREN SEMICOLON'''
    rules.sortMatrix(p)
    
    
def p_media(p):
    '''media : MEDIA LEFTPAREN ID RIGHTPAREN'''
    rules.media(p)
    
    
def p_moda(p):
    '''moda : MODA LEFTPAREN ID RIGHTPAREN'''
    rules.moda(p)
    
    
def p_mediana(p):
    '''mediana : MEDIANA LEFTPAREN ID RIGHTPAREN'''
    rules.mediana(p)
    

def p_return(p):
    '''return : RETURN recursion SEMICOLON
              | RETURN ID SEMICOLON
              | RETURN SEMICOLON'''
              
              
# TODO ARREGLAR RECURSION
def p_recursion(p):
    '''recursion : LEFTPAREN recursion RIGHTPAREN
                 | ID LEFTPAREN recursion RIGHTPAREN recursion
                 | PLUS recursion
                 | MINUS recursion
                 | var_cte PLUS var_cte
                 | var_cte MINUS var_cte
                 | var_cte
                 | empty'''



# ╭──────────────────────────────────────────────────────────────╮
# │                            ERRORS                            │
# ╰──────────────────────────────────────────────────────────────╯

def p_error(p):
    # raise TypeError("Syntax error in input! - {} ".format(p)) # Para detener la compilación
    print("Syntax error in input! - {} ".format(p))


def p_empty(p):
    '''empty :'''
    pass



# ╭──────────────────────────────────────────────────────────────╮
# │                            READER                            │
# ╰──────────────────────────────────────────────────────────────╯

import sys
import ply.yacc as yacc

from Lexer import tokens

yacc.yacc()

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if yacc.parse(data) == "COMPILED":
                print("Compilation Completed")
        except EOFError:
            print(EOFError)
    else:
        print("File not found")