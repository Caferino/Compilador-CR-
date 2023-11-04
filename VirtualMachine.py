"""
    Proyecto Final
    Autor: Óscar Antonio Hinojosa Salum A00821930
    Mayo 28 2023
    Compilador para lenguaje al estilo R/C++.

    --- VM / Virtual Machine / Máquina Virtual ---
"""

# ======================== Virtual Machine ======================== #

from functools import reduce
"""import operator
import sys""" # ! Borrar
import pprint
import re

class VirtualMachine:
    def __init__(self):
        self.memorySize = 500
        self.registers = [None] * self.memorySize
        self.registers[0] = "GOTO MAIN"
        self.stack = [] # ! Donde se usa??
        self.functionJumps = []
        self.program_counter = 0
        self.quadruples = []
        self.symbolTable = []


    def start(self, quadruples, newSymbolTable):
        self.quadruples = quadruples
        self.symbolTable = newSymbolTable
        self.run()


    def run(self):
        '''
        Input: Cuádruplos en forma de tuplas tipo:
            [operador, operandoIzquierdo, operandoDerecho, dondeInsertarResultado]

        Output: Resultados del programa.
        '''
        while self.program_counter < len(self.quadruples):
            quadruple = self.quadruples[self.program_counter]
            operator, operand1, operand2, target = quadruple

            # Qué asco ya sé, una búsqueda lineal O(n) por cada operando que sea una variable...
            # Si nuestro resultado será un espacio temporal, lo "hacemos" índice (t1 = 1, t82 = 82, ...)
            # "t0", al "no existir", lo dejé reservado para el GOTO MAIN por si acaso y mientras
            if isinstance(target, str) and re.match(r"^t\d+$", target) : 
                target = int(target[1:])
                # self.registers.append(target)

            # Si nuestro operando izquierdo es un espacio temporal ...
            if isinstance(operand1, str) and re.match(r"^t\d+$", operand1) : 
                operand1 = self.registers[int(operand1[1:])]
            # Si no, debe ser un ID cuyo valor debemos sacar de la SymbolTable
            elif isinstance(operand1, str):
                for tuple in self.symbolTable :
                    if operand1 == tuple[1] :
                        # Si es una lista de un solo elemento, sacarlo
                        if isinstance(tuple[6], list) and len(tuple[6]) == 1 : operand1 = tuple[6][0]
                        # Si sufrió alguna actualización antes de aquí, lo más seguro es
                        # que ya no es una lista de un elemento, sino número o string ...
                        else : operand1 = tuple[6]
                        break

            # Para lidiar con condicionales, el problema de bool() es que si es una string
            # con valor de 'False' la convierte a un booleano True porque lo que checa es que
            # la string está vacía o no. El que nos interesa es eval(), pero solo funciona con
            # strings; no importa si usamos bool() para valores numéricos
            if operand1 == 'True' or operand1 == "False" :
                operand1 = eval(operand1)

            # Si nuestro operando derecho es un espacio temporal ...
            if isinstance(operand2, str) and re.match(r"^t\d+$", operand2) : 
                operand2 = self.registers[int(operand2[1:])]
            # Si no, debe ser un ID cuyo valor debemos sacar de la SymbolTable
            elif isinstance(operand2, str):
                for tuple in self.symbolTable :
                    if operand2 == tuple[1] :
                        # Si es una lista de un elemento, sacarlo
                        if isinstance(tuple[6], list) : operand2 = tuple[6][0]
                        else : operand2 = tuple[6]
                        break

            if operand2 == 'True' or operand2 == "False" :
                operand2 = eval(operand2)

            if operand1 == None : operand1 = 1
            if operand2 == None : operand2 = 1


            # ======= REGISTERS ========
            if operator == '+' :
                self.registers[target] = operand1 + operand2
            elif operator == '-' :
                self.registers[target] = operand1 - operand2
            elif operator == '*' :
                self.registers[target] = operand1 * operand2
            elif operator == '**' :
                self.registers[target] = operand1 ** operand2
            elif operator == '/' :
                self.registers[target] = operand1 / operand2
            elif operator == '>' :
                self.registers[target] = int(operand1 > operand2)
            elif operator == '<' :
                self.registers[target] = int(operand1 < operand2)
            elif operator == '<=' :
                self.registers[target] = int(operand1 <= operand2)
            elif operator == '==':
                self.registers[target] = bool(operand1) == bool(operand2)
            elif operator == '!=' or operator == '<>':
                self.registers[target] = bool(operand1) != bool(operand2)
            if operator == '&&':
                self.registers[target] = bool(operand1) and bool(operand2)
            if operator == '||':
                self.registers[target] = bool(operand1) or bool(operand2)
            elif operator == '=' or operator == '<-' :
                # Si es un string, es porque a fuerza es un ID ...
                if target.__class__.__name__ == 'str' :
                    for i, tuple_item in enumerate(self.symbolTable):
                        if target == tuple_item[1]:
                            currentRow = self.symbolTable[i]
                            # Actualizamos la columna "value"
                            index_to_change = 6
                            currentRow = currentRow[:index_to_change] + (operand1,)
                            self.symbolTable[i] = currentRow
                            # En caso de haberse transformado de INT a FLOAT, actualizar TYPE
                            if currentRow[0] != operand1.__class__.__name__ :
                                currentRow = (operand1.__class__.__name__,) + currentRow[1:]
                                self.symbolTable[i] = currentRow

                # Si no, es el index de un espacio temporal
                else:
                    self.registers[target] = operand1
            elif operator.lower() == 'goto':
                self.program_counter = target
                continue
            elif operator.lower() == 'gotof':
                if operand1 == 'False' or operand1 == 0 : self.program_counter = target
                else : self.program_counter += 1
                continue
            elif operator.lower() == 'gotov':
                # Aquí se me ocurrió cambiar el chequeo de booleanos igual a Python o C++ :
                # if num != 0 = TRUE, else FALSE no matter what
                if operand1 == 'True' or operand1 != 0 : self.program_counter = target
                else : self.program_counter += 1
                continue
            elif operator.lower() == 'print':
                if isinstance(operand1, list):
                    for index, element in enumerate(operand1) :
                        if isinstance(element, str) and re.match(r"^t\d+$", element) : 
                            operand1[index] = str(self.registers[int(element[1:])])
                    operand1 = " ".join(reversed(operand1))
                print(operand1.strip('"')) if operand1.__class__.__name__ == 'str' else print(operand1)
            elif operator.lower() == 'gosub':
                self.program_counter = target
                self.functionJumps.append(operand2)
                continue
                # Meter el salto de la linea en la que estaba...
                # PJumps... No estoy seguro
            elif operator.lower() == 'endfunc' or operator.lower() == 'return':
                if self.functionJumps : 
                    self.program_counter = self.functionJumps.pop()
                    continue
                # PJumps...
                # Hacer el salto a la linea en la que estaba...
            elif operator.lower() == 'endprog':
                if operand1:
                    print("v v v v v v    === DEBUGGING ===    v v v v v v")
                    print("-------------- === Final Quadruples === --------------")
                    for i, item in enumerate(self.quadruples):
                        print(f"{i}: {item}")
                    print("-------------- === Final Symbol Table (Updated Values) === --------------")
                    pprint.pprint(self.symbolTable)
                print('Compilation Completed')
            elif operator.lower() == 'era':
                print('ERA LOGIC HERE')
            elif operator.lower() == 'test':
                print('TEST HERE')
            """elif operator.lower() == 'return':
                return_value = self.registers[operand1]
                self.program_counter = self.functionJumps.pop()
                self.registers[target] = return_value
                continue
                if self.functionJumps :
                    self.program_counter = self.functionJumps[-1]
                    continue"""

            self.program_counter += 1