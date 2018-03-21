# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:21:56 2018

@author: ALVARO
"""
import random, re

def main():
    matriz = getTextFromFile("corpus.txt")

    print("tamaño matriz: ", str(len(matriz)))
    print("tamaño 0.8 de los datos(matriz): ", str(int(len(matriz)*0.8)), "\n")
    
    training = randomSample(matriz, 0.8)
    test = randomSample(matriz, 0.5)
    cross_validation = randomSample(matriz, 1)
      
    print("tamaño training: ", str(len(training)))    
    print("tamaño test: ", str(len(test)))
    print("tamaño cross: ", str(len(cross_validation)), "\n")
    
    ham_training = classifyMessages(training, 'ham')
    spam_training = classifyMessages(training, 'spam')
    
    print("size ham_training: ", str(len(ham_training)))
    print("size spam_training: ", str(len(spam_training)))
    
    ham_words = getUniqueWords(ham_training)
    spam_words = getUniqueWords(spam_training)
    
    print("size unique ham words:", len(ham_words))
    print("size unique spam words", len(spam_words))
    
def getTextFromFile(file_name, sanit=True, log=False):
    matriz = []
    data = [line.strip() for line in open(file_name, 'r')]
    for i in range(len(data)):
        columna = []
        x, y =  data[i].split("\t")
        columna.append(x)
        if (sanit):
            columna.append(sanitizar(y)) 
        else: 
            columna.append(y)
        matriz.append(columna)
    
    if (log):
        for j in range(len(data)):
            print(matriz[j])
        print("\n")
    return matriz

def randomSample(matriz, percentage):
    salida = []
    for _ in range(0, int((len(matriz))*percentage)):
       salida.append(matriz.pop(random.randrange(0, len(matriz)))) #randrange en vez de randint(lower bound)
    return salida

def sanitizar(cadena_entrada):
    return ((re.sub('[^A-Za-z0-9 ]+', '', cadena_entrada)).lower())

def classifyMessages(matriz, etiqueta_mensaje):
    salida = []
    for i in range(len(matriz)):
        tupla = matriz[i]
        if(tupla[0]==etiqueta_mensaje):
            salida.append(tupla[1])
    return salida

def getUniqueWords(array):
    salida = []
    for i in range(len(array)):
        phrase = array[i].split(" ")
        for word in phrase:
            if word not in salida:
                salida.append(word)
    return salida
main()