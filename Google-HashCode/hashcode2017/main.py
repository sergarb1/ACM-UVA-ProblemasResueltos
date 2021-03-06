#!/usr/bin/python3
import random
import json
import sys
import os
from heapq import merge

#devcuelve mejor cache para endpoint de ese video y que quepa

def obtenerMejorCacheYCabe(nEnd,nVid):
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    resultado=-1
    mejorLat=9999

    for i in range(C):
        if(cuantoLibre(i)>int(videos[nVid])):
            if i in dicEndCache:
                if nEnd in dicEndCache[i]:
                    lat=dicEndCache[i][nEnd]
                    if lat<mejorLat:
                        mejorLat=lat
                        resultado=i


    if resultado==-1:
        return None
    else:
        return resultado


#devuelve el numero de video mejor para ese endpoint algoritmo 2

def obtenerMejor2(nEnd):
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    max=-1
    maxN=-1

    if nEnd in dicEndVideo:
        for j in dicEndVideo[nEnd]:
            if int(videos[j])>X:
                continue
            #1 tam=int(videos[j])*int(dicEndVideo[nEnd][j])
            #2 tam=int(dicEndVideo[nEnd][j])
            tam=int(dicEndVideo[nEnd][j])*int(dicEndCentral[nEnd][0])

            #print("Para endpoint "+str(nEnd)+" video  "+str(j)+ " con tam "+str(tam))
            if(tam>max):
                max=tam
                maxN=j

        if max>-1:
            return maxN
        else:
            return None


    else:
        return None


#devuelve el numero de video mejor para ese endpoint algoritmo 2

def obtenerMejor(nEnd):
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    max=-1
    maxN=-1

    if nEnd in dicEndVideo:
        for j in dicEndVideo[nEnd]:
            if int(videos[j])>X:
                continue
            #1 tam=int(videos[j])*int(dicEndVideo[nEnd][j])
            tam=int(dicEndVideo[nEnd][j])
            #3 tam=int(dicEndVideo[nEnd][j])*int(dicEndCentral[nEnd])

            #print("Para endpoint "+str(nEnd)+" video  "+str(j)+ " con tam "+str(tam))
            if(tam>max):
                max=tam
                maxN=j

        if max>-1:
            return maxN
        else:
            return None


    else:
        return None


def obtenerRequestVideoEstrella(nEnd):

    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado
    tam=0
    for i in dicEndVideo[nEnd]:
        tam=tam+int(dicEndVideo[nEnd][i])
    return tam

def funcionOrdenarLatencias(elemento):
    return elemento[0]


def funcionOrdenarRequest(elemento):
    return obtenerRequestVideoEstrella(elemento[1])

def funcionOrdenarRequestLatencias(elemento):
    return elemento[0]*obtenerRequestVideoEstrella(elemento[1])


def primeroMaximo():
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    #Ordenar por latencia

    dicEndCentral.sort(key=funcionOrdenarRequest,reverse=True)
    rango=[]
    for i in dicEndCentral:
        rango.append(i[1])



    for j in rango:
        while True:
            laMejor=obtenerMejor(j)
            #print("El mejor para "+str(j)+" es "+str(laMejor))
            if laMejor is None:
                break

            #escoger cache mas rapida disponible para ese endpoint y que quepa

            nCache=obtenerMejorCacheYCabe(j,laMejor)

            if nCache==None:
                break
            else:
                if nCache in dicResultado:
                    if laMejor not in dicResultado[nCache]:
                        dicResultado[nCache].append(laMejor)
                else:
                    dicResultado[nCache] = [laMejor]

            #cargarse la request
            dicEndVideo[j].pop(laMejor, None)

def primeroMaximo2():
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    #Ordenar por latencia

    dicEndCentral.sort(key=funcionOrdenarRequest,reverse=True)
    rango=[]
    for i in dicEndCentral:
        rango.append(i[1])



    for j in rango:
        while True:
            laMejor=obtenerMejor2(j)
            #print("El mejor para "+str(j)+" es "+str(laMejor))
            if laMejor is None:
                break

            #escoger cache mas rapida disponible para ese endpoint y que quepa

            nCache=obtenerMejorCacheYCabe(j,laMejor)

            if nCache==None:
                break
            else:
                if nCache in dicResultado:
                    if laMejor not in dicResultado[nCache]:
                        dicResultado[nCache].append(laMejor)
                else:
                    dicResultado[nCache] = [laMejor]

            #cargarse la request
            dicEndVideo[j].pop(laMejor, None)



def primeroMejorRequest():
    return 0



def cuantoLibre(numCache):
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    if numCache not in dicResultado:
        return X

    lista=dicResultado[numCache]

    res=0
    for i in range(len(lista)):
        res=res+int(videos[lista[i]])


    return X-res



def primeroCabe():
    global V, E, R, C, X, videos, dicEndCache, dicEndCentral, dicEndVideo, dicResultado

    rV=[]
    rC=[]
    for i in range(V):
        rV.append(i)

    for i in range(C):
        rC.append(i)

    random.shuffle(rV)

    random.shuffle(rC)

    for i in range(V):
        for j in range(C):
            if cuantoLibre(j)>int(videos[i]):
                if j  in dicResultado:
                    if i not in dicResultado[j]:
                        dicResultado[j].append(i)
                else:
                    dicResultado[j]=[i]



#main
def main():

    #Variables globales que necesitan ser escrita
    global V,E,R,C,X,videos,dicEndCache,dicEndCentral,dicEndVideo,dicResultado

    V, E, R, C, X=map(int, input().split())

    videos=(input().split())


    dicResultado={}
    #hola google

    #Aqui las latencias y la latencia del endpoint sevidor
    #Latencia de el endpoint con los servidores cache que tengan (pueden ser 0)
    dicEndCache={}
    #Latencia endpoint con servidor
    dicEndCentral=[]
    #Diccionario que guarda numero de peticiones desde un endpoint  de un video
    dicEndVideo={}


    for i in range(E):
        LCentral, Ncaches = map(int, input().split())
        dicEndCache[i]={}

        dicEndCentral.append([LCentral,i])
        for j in range(Ncaches):
            Ecache, Lcache = map(int, input().split())
            dicEndCache[i][Ecache]=Lcache

    #Ordenamos endpoints por orden mayor latencia



    #Request
    for i in range(R):
        Nvideo, Evideo, Nrequest = map(int, input().split())
        if Evideo in dicEndVideo:
            if Nvideo in dicEndVideo[Evideo]:
                dicEndVideo[Evideo][Nvideo] =dicEndVideo[Evideo][Nvideo]+ Nrequest
            else:
                dicEndVideo[Evideo][Nvideo]=Nrequest
        else:
            dicEndVideo[Evideo]={}
            dicEndVideo[Evideo][Nvideo] = Nrequest
    '''
    print("Endpoints to cache")
    print(dicEndCache)
    print("Endpoints to central")

    print(dicEndCentral)
    print("Endpoins and videos")

    print (dicEndVideo)

    '''
    primeroMaximo()
    primeroMaximo2()
    primeroCabe()

    print(len(dicResultado))
    for i in dicResultado:
        cadena=str(i)
        for j in range(len(dicResultado[i])):
            cadena=cadena+" "+str(dicResultado[i][j])

        print(cadena)




if __name__ == "__main__":
    # execute only if run as a script
    main()