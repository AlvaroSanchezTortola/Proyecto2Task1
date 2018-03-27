# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:21:56 2018

@author: ALVARO
"""
import FuncionesTask1 as fun

def main():
    matriz = fun.getTextFromFile("corpus.txt")

    print("tamaño matriz: ", str(len(matriz)))
    print("tamaño 0.8 de los datos(matriz): ", str(int(len(matriz)*0.8)), "\n")
    
    training = fun.randomSample(matriz, 0.8)
    test = fun.randomSample(matriz, 0.5)
    cross_validation = fun.randomSample(matriz, 1)
      
    print("tamaño training: ", str(len(training)))    
    print("tamaño test: ", str(len(test)))
    print("tamaño cross: ", str(len(cross_validation)), "\n")
    
    ham_training = fun.classifyMessages(training, 'ham')
    spam_training = fun.classifyMessages(training, 'spam')
    
    print("size ham_training: ", str(len(ham_training)))
    print("size spam_training: ", str(len(spam_training)))
    
    ham_words = fun.getUniqueWords(ham_training)
    spam_words = fun.getUniqueWords(spam_training)
    
    print("size unique ham words:", len(ham_words))
    print("size unique spam words", len(spam_words))
    
    total_words_training = fun.getUniqueWords(fun.getColumna(training, 1))
    print("total unique words training: ", len(total_words_training))
    
    prueba = ["this", "is", "spam"]
    #prueba = fun.readEntryFile("prueba.txt", True, False)
    print(prueba)
    
    prob_spam = fun.propabilidadTotal(prueba[0], 1, "spam", ham_words, spam_words, len(total_words_training), training)
    prob_ham = fun.propabilidadTotal(prueba[0], 1, "ham", ham_words, spam_words, len(total_words_training), training)    
    print("probabilidad spam: ", prob_spam, "\n", "probabilidad ham: ", prob_ham)
    
    mejor_i = 0
    mejor_accuracy = 0.0
    for j in range(1,10):
        #Iterar y obtener accuracy por un i ---------
        aciertos = 0
        i_actual = j
        print ("para este i: ", i_actual)
        for i in range(len(test)):
            tupla = test[i]
            actual_label = tupla[0]
            phrase = fun.sanitizar(tupla[1])
            phrase_words = phrase.split(" ")
            
            print ("i: ", i_actual," iter: ", i, ": ", phrase)
            
            prob_spam = fun.propabilidadTotal(phrase_words, i_actual, "spam", ham_words, spam_words, len(total_words_training), training)
            prob_ham = fun.propabilidadTotal(phrase_words, i_actual, "ham", ham_words, spam_words, len(total_words_training), training) 
            predicted = ""
            if(prob_spam > prob_ham): predicted = "spam"
            elif(prob_spam < prob_ham): predicted = "ham"
            if(actual_label==predicted): aciertos+=1
        
        accuracy = aciertos/len(test)
        print("\nAccuracy en test: ", accuracy)
        #-----------------------------------------------
        if (accuracy > mejor_accuracy):
            mejor_accuracy = accuracy
            mejor_i = i_actual
    print("\nMejor i y accuracy: ", mejor_i, ": ", mejor_accuracy)
main()