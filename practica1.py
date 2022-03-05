##########################################
#Author: Monica Ocaña Bastante
#Date: 2021/10/20
#Este es un algoritmo genetico modular, en el que se debe especificar
#el numero de genes (bits) y la funcion de fitness (debe ser una url)
#
#El grado de mutacion, tamaño de poblacion es customizable, haciendo el cruce
#punto a punto y la seleccion mediante torneos (la variable torneos guarda el numero 
# de individuos que participan)
# Para evitar fallos, decida donde quiere guardar los archivos que genera el programa
#######################################
import requests 
import random as r
#####################################################
#VARIABLES##############VARIABLES####################
#####################################################
#ficheros auxiliares
mejores = open("evolucionPoblacion.txt","a")
csv = open("datosFitness.csv","a")
csv2 = open ("datosGlogales.csv","a")
#parametros
parada = 2000 #criterio de parada (iteraciones maximas)
bandera = False #segundo criterio de parada
rondasMax = 10 #numero de rondas seguidas donde el mejor no cambia y por tanto debe saltar la bandera
rondas = 0
gradoMutacion= 0.01 #porcentaje
sizepoblacion = 500 #embergadura de poblacion
sizeCromosoma = 384 #longitud de cromosomas
torneo = int(sizepoblacion*0.05) #numero individuos en el torneo
web ='http://memento.evannai.inf.uc3m.es/age/pilar?c=' #pagina con la funcion
sumarTorneo=int(sizepoblacion*0.05)
#contadores
i = 0
j = 0
x = 0
cr = 0 #ciclos de cromosomas

#auxiliares
sensor = False      # False el mejor no ha cambiado, True ha cambiado
min = 0.0           #minimo de torneo
crMejor = 0         #cromosoma da minimo en ese torneo (posicion en array de poblacion de torneo)
mejor = 0.0         #valor minimo total de todas las generacios
mejorGeneracion = 0.0     #mejor valor de una generacion concreta
crMejorGen = [0]*sizeCromosoma    #mejor cromosoma de una generacion
cromosomaMejor = [0]*sizeCromosoma    #cromosoma que da mejor resultado
cromosoma = ""    #guardar el cromosoma que se va a probar para la pagina
numero = 0 #guardar numeros 
mutacion= 0.0
conectado=False
#####################################################
#VARIABLES##############VARIABLES####################
#####################################################



#Inicializamos la matriz de la poblacion inicial de cada ciclo
#son tan largos como un cromosoma mas un espacio extra para poder guardar el valor de fitnnes del individuo
poblacionInicial = []
for i in range(sizepoblacion):
    a = [0]*(sizeCromosoma+1)
    poblacionInicial.append(a)
#poblacion obtenida en los torneos
poblacion=[]
for i in range(sizepoblacion):
    a = [0]*(sizeCromosoma)
    poblacion.append(a)
poblacionTorneo=[]
for i in range(torneo):
    a = [0]*(sizeCromosoma+1)
    poblacionTorneo.append(a)
i = 0
x = 0
numero = 0
#crear poblacion inicial
# inicial
for i in range(sizepoblacion):
    for x in range(sizeCromosoma):
        numero=r.randint(0,1)
        poblacionInicial[i][x]=numero
    x=0
i = 0
x = 0



#reinicio de contadores para asegurar que todos los bucles se hacen bien
i=0
j=0
x=0
cr=0
cromosoma=""
mejores.write("Rondas: "+str(parada)+", Individuos: "+str(sizepoblacion)+", Maximo rondas: "+str(rondasMax)+"\n")
mejores.write("Mutacion: "+str(gradoMutacion)+", Torneos: "+str(torneo)+"\n")
mejores.write("Evolucion de la poblacion:\n")
csv.write("Mejor Generacion; Mejor absoluto\n")
#BUCLE PRINCIPAL
while(i<parada and not bandera):
    #####################################################
    #EVALUACION###################EVALUACION#############
    #####################################################
    sensor=False
    print("Generacion "+str(i))
    print("Evaluacion")
    #calcular mejor inicial de esta generacion
    for cr in range(sizeCromosoma):
        cromosoma=cromosoma+str(poblacionInicial[0][cr])
    conectado=False
    while not conectado:
        try:
            resultado=requests.get(web + cromosoma)
            conectado=True
        except:
            conectado=False
            print("Fallo de conexion. Volviendo a intentar")
    cromosoma=""
    mejores.write("Ronda "+str(i)+":\n")
    mejorGeneracion=float(resultado.text)+100.0
    for x in range(sizeCromosoma):
        crMejorGen[x]=poblacionInicial[0][x]
    x=0
    #comprobar individuo por individuo su valor
    for j in range(sizepoblacion):
        for cr in range(sizeCromosoma):
            cromosoma=cromosoma+str(poblacionInicial[j][cr])
        conectado=False
        while not conectado:
            try:
                resultado=requests.get(web + cromosoma)
                conectado=True
            except:
                conectado=False
                print("Error de conexion. Probando otra vez")
        cromosoma=""
        poblacionInicial[j][sizeCromosoma]=resultado
        #Si es el primero de todas las generaciones,
        #su valor es la base para hacer de mejor absoluto con el que comparar
        if(i==0 and j==0):
            mejor=float(resultado.text)
            mejorGeneracion=float(resultado.text)
            for x in range(sizeCromosoma):
                crMejorGen[x]=poblacionInicial[j][x]
                cromosomaMejor[x]=poblacionInicial[j][x]
            x=0
        #ver si el resultado es mejor comparado con el resto
        else:
            #ver si es el mejor absoluto
            if(float(resultado.text)<mejor):
                sensor=True
                mejor=float(resultado.text)
                for x in range(sizeCromosoma):
                    cromosomaMejor[x]=poblacionInicial[j][x]
                x=0
            #ver si es el mejor de la generacion actual
            if(float(resultado.text)<mejorGeneracion):
                mejorGeneracion=float(resultado.text)
                for x in range(sizeCromosoma):
                    crMejorGen[x]=poblacionInicial[j][x]
                x=0
        cr=0
    j=0
    #escribir resultado de esta generacion
    mejores.write("Generacion "+str(i)+":\nMejor de la generacion: "+str(crMejorGen)+"\nCon valor: "+str(mejorGeneracion)+"\nMejor hasta el momento: "+str(cromosomaMejor)+"\nCon valor: "+str(mejor)+"\n")
    csv.write(str(mejorGeneracion)+";"+str(mejor)+"\n")
    #comprobar si el mejor absoluto ha cambiado
    if(not sensor):
        rondas+=1
        print("Mejor valor de la generacion: "+str(mejorGeneracion))
        #si lleva mas de rondasMax sin cambiar, la poblacion se ha estancado y se sale del bucle principal
        if(rondas>rondasMax):
            print("Tenemos una gran solucion")
            mejores.write("La mejor solucion lleva sin cambiar mas del tope, por tanto hemos parado de buscar")
            bandera=True
            print("Mejor valor ganador: "+str(mejor))
    else:
        #restaurar valor e imprimer valores actuales de mejores 
        sensor=False
        rondas=0
        print("Mejor valor: "+str(mejor))
        print("Mejor valor de la generacion: "+str(mejorGeneracion))
    #####################################################
    #TORNEO###################TORNEO#####################
    #####################################################
    print("Torneos")
    for j in range(sizepoblacion):
        #seleccionar gente para el torneo.Un torneo por individuo nuevo
        for x in range(torneo):
            numero=r.randint(0,(sizepoblacion-1))
            for cr in range(sizeCromosoma):
                poblacionTorneo[x][cr]=poblacionInicial[numero][cr]
            cr=0
            poblacionTorneo[x][sizeCromosoma]=poblacionInicial[numero][sizeCromosoma]
        x=0
        crMejor=0
        #escoger el mejor del torneo
        for x in range(torneo):
            cromosoma=""
            for cr in range(sizeCromosoma):
                cromosoma=cromosoma+str(poblacionTorneo[x][cr])
            cr=0
            resultado=poblacionTorneo[x][sizeCromosoma]
            if(x==0):
                min=float(resultado.text)
                crMejor=0
            elif(float(resultado.text)<min):
                min=float(resultado.text)
                crMejor=x
        cromosoma=""
        cr=0
        #si es la mejor solucion hasta el momento, guardarla
        if(min<mejor):
            mejor=min
            for cr in range(sizeCromosoma):
                cromosomaMejor[cr]=poblacionTorneo[crMejor][cr]
            mejores.write("Cromosoma: "+str(cromosomaMejor)+", Valor: "+str(mejor)+", Generacion: "+str(i))
        min=0
        cr=0
        #el mejor pasa a la nueva poblacion
        for cr in range(sizeCromosoma):
            poblacion[j][cr]=poblacionTorneo[crMejor][cr]
        cr=0
        crMejor=0
        x=0
    j=0

    #####################################################
    #CRUCE###################CRUCE#######################
    #####################################################
    print("Cruce")
    j=0
    x=0
    for j in range(sizepoblacion):
        for x in range(sizeCromosoma):
            if(j%(2)==0):
                if(x<sizeCromosoma/2):
                    poblacionInicial[j][x]=poblacion[j][x]
                else:
                    poblacionInicial[j][x]=poblacion[j+1][x]
            else:
                if(x<sizeCromosoma/2):
                    poblacionInicial[j][x]=poblacion[j][x]
                else:
                    poblacionInicial[j][x]=poblacion[j-1][x]
        x=0
    j=0
    #####################################################
    #MUTACION#############MUTACION#######################
    #####################################################
    print("Mutacion")
    j=0
    x=0
    cr=0

    for j in range(sizepoblacion):
        for x in range(sizeCromosoma):
            mutacion=r.random()
            if(mutacion<=gradoMutacion): #si se cumple proporcion, se realiza la mutacion. Gen por gen
                if(poblacionInicial[j][x]==0):
                    poblacionInicial[j][x]=1
                else:
                    poblacionInicial[j][x]=0
        x=0
    #####################################################
    #            VARIABLES DE CONTROL DEL BUCLE         #
    #####################################################
    x=0
    j=0
    cr=0
    i+=1 
#FIN DEL BUCLE PRINCIPAL
#escribir mejores datos
csv2.write("rondasMax;individuos;cromosoma;torneos;mutacion;mejor;mejorGeneracion,generaciones\n") #comentar esta linea despues de la primera generacion para no hacer encabezado
csv2.write(+str(rondasMax)+";"+str(sizepoblacion)+";"+str(sizeCromosoma)+";"+str(torneo)+";"+str(gradoMutacion)+";"+str(mejor)+";"+str(mejorGeneracion)+";"+str(i-1)+"\n")
#cerramos todos los ficheros    
mejores.close()  
csv.close()
csv2.close()