# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 14:00:35 2018

@author: ALVARO
"""
import random, re
    
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

def getColumna(matriz, num_columna):
    salida = []
    for i in range(len(matriz)):
        tupla = matriz[i]
        salida.append(tupla[num_columna])
    return salida
"""
INPUT: int K, string palabra, array tipo_palabra, int palabras_totales
"""
def laplaceSmoothingBasic(k, palabra, tipo_palabra, palabras_totales):
    cant_ocurrencia = 0.0
    cant_observaciones = len(tipo_palabra)
    for i in range(len(tipo_palabra)):
        if tipo_palabra[i]==palabra: cant_ocurrencia +=1
    return ((cant_ocurrencia + k)/(cant_observaciones + k*palabras_totales))

"""
INPUT: array string mensajes, int k, array tipo_palabra, int palabras_totales
"""
def probabilidadOracion(mensaje, k, tipo_palabra, palabras_totales):
    probabilidad = 1.0
    for i in range(len(mensaje)):
        probabilidad =  probabilidad * laplaceSmoothingBasic(k, mensaje[i], tipo_palabra, palabras_totales)
    return probabilidad

"""
INPUT: matriz grupo, string tipo, int k
"""
def probabilidadMain(grupo, tipo, k):
    cant_ocurrencia = 0.0
    cant_observaciones = len(grupo)
    for i in range(len(grupo)):
        tupla = grupo[i]
        if(tupla[0]==tipo): cant_ocurrencia += 1
    return ((cant_ocurrencia + k)/(cant_observaciones + k*2))

"""
INPUT: array de strings, int k, "spam" o "ham", array palabras de ham, array palabras de spam, int palabras totales, matriz de etiqueta con frases
"""
def propabilidadTotal(mensaje, k, objetivo, tipo_ham, tipo_spam, palabras_totales, grupo):
    parte1 =  probabilidadOracion(mensaje, k, tipo_spam, palabras_totales)*probabilidadMain(grupo, "spam", k)
    parte2 =  probabilidadOracion(mensaje, k, tipo_ham, palabras_totales)*probabilidadMain(grupo, "ham", k)
    #print(parte1, parte2)
    if(parte1==0.0): parte1 = 0.0000000001
    if(parte2==0.0): parte2 = 0.0000000001
    
    if (objetivo=="spam"): return ((parte1)/(parte1 + parte2))
    elif(objetivo=="ham"): return ((parte2)/(parte2 + parte1))
    
def readEntryFile(file_name, sanit=True, log=False, split=False):
    matriz = []
    data = [sanitizar(line.strip()) for line in open(file_name, 'r')]
    for i in range(len(data)):
        columna = []
        if(split): phrase = data[i].split(" ")
        else: phrase = data[i]
        columna.append(phrase)
        matriz.append(columna)
    
    if (log):
        for j in range(len(data)):
            print(matriz[j])
        print("\n")
    return matriz

def generateOutputMatrix(input_matrix, i_actual, ham_words, spam_words, len_total_words_training, training_group, log=False ):
    salida = []
    for i in range(len(input_matrix)):
        tupla_salida = []
        tupla = input_matrix[i]
        
        if(len(tupla)==2): phrase = sanitizar(tupla[1])
        elif(len(tupla)==1): phrase = sanitizar(tupla[0])
        phrase_words = phrase.split(" ")
        
        if(log): print ("i: ", i_actual," iter: ", i, ": ", phrase)
        
        prob_spam = propabilidadTotal(phrase_words, i_actual, "spam", ham_words, spam_words, len_total_words_training, training_group)
        prob_ham = propabilidadTotal(phrase_words, i_actual, "ham", ham_words, spam_words, len_total_words_training, training_group) 
        predicted = ""
        if(prob_spam > prob_ham): predicted = "spam"
        elif(prob_spam <= prob_ham): predicted = "ham"
        
        tupla_salida.append(predicted)
        tupla_salida.append(phrase)
        salida.append(tupla_salida)
    return salida
            
def getAccuracy(matrix_to_evaluate, base_matrix, log=False):
    #if(len(matrix_to_evaluate)!=len(base_matrix)):
    #    print("MATRICES DIFERENTES LEN")
    #else:
        aciertos = 0
        for i in range(len(matrix_to_evaluate)):
            tupla_to_evaluate = matrix_to_evaluate[i]
            tupla_base = base_matrix[i]         
            if (log): print(tupla_to_evaluate[0], tupla_base[0])
            if(tupla_to_evaluate[0]==tupla_base[0]):
                aciertos += 1
        return (aciertos/len(matrix_to_evaluate))
 

def writeOutput(matrix, name):
    file = open(name, "w")
    for i in range(len(matrix)):
        tupla = matrix[i]
        file.write(str(tupla[0])+" \t"+str(tupla[1])+"\n")  
    file.close()