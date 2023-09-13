#Importa librería sys:
import sys

#Obtiene los argumentos de línea de comandos con sys.argv
args = sys.argv

#Verifica si hay más de 2 args:
#Si sí, imprime un saludo con los dos primeros args:
if len(args) > 2:
    print("Good %s, %s" % (args[1],args[2]))
#Si no, pide más args y sale
else:
    print("I need more args!")
    quit()


#Ejecutarlo en terminal, como: 
# python argsysN1k0.py arg1 arg2 => Good arg1, arg2
# python argsysN1k0.py => I need more args!