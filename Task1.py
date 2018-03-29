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
    print("total unique words training: ", len(total_words_training), "\n")
    
    """ #Prueba 
    prueba = ["this", "is", "spam"]
    #prueba = fun.readEntryFile("prueba.txt", True, False)
    print(prueba)
    
    prob_spam = fun.propabilidadTotal(prueba[0], 1, "spam", ham_words, spam_words, len(total_words_training), training)
    prob_ham = fun.propabilidadTotal(prueba[0], 1, "ham", ham_words, spam_words, len(total_words_training), training)    
    print("probabilidad spam: ", prob_spam, "\n", "probabilidad ham: ", prob_ham, "\n")
    """
    #--Cross Validation Phase---
    mejor_i, mejor_accuracy = 0, 0.0
    
    for i in range(1,10):
        salida_cross = fun.generateOutputMatrix(cross_validation, i, ham_words, spam_words, len(total_words_training), training, True)
        accuracy = fun.getAccuracy(salida_cross, cross_validation)
        if (accuracy > mejor_accuracy): mejor_accuracy, mejor_i = accuracy, i
    print("\nCROSS VALIADTION: Mejor i y accuracy: ", mejor_i, ": ", mejor_accuracy)
    
    #--Test Phase---
    salida_test = fun.generateOutputMatrix(test, mejor_i, ham_words, spam_words, len(total_words_training), training, True)
    test_acc = fun.getAccuracy(salida_test, test)
    print("\nTEST: i y accuracy: ", mejor_i, ": ", test_acc, "\n")
    
    #--Input Phase---
    input_file = fun.readEntryFile("prueba.txt", True, False, False)
    salida_input = fun.generateOutputMatrix(input_file, mejor_i, ham_words, spam_words, len(total_words_training), training, True)
    fun.writeOutput(salida_input, "output.txt")

main()