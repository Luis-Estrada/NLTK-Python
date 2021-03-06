#Enlace al Dataset utilizado: http://www.sngularmeaning.team/TASS2015/tass2015.php#contact

import nltk
import random
import pickle
import time

from nltk.classify import ClassifierI
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

tiempo_inicio = time.time()

def leer_archivo(ruta):
    frases = []
    frases_archivo = open(ruta,"r", encoding="utf8").read()
    
    return frases_archivo

def etiquetar_datos(frases_pos, frases_neg):
    datos = []

    for f in frases_pos.split('\n'):
        datos.append((f, "pos"))
    for f in frases_neg.split('\n'):
        datos.append((f, "neg"))

    random.shuffle(datos)

    return datos

def tokenizar_dataset(frases_pos, frases_neg):
    tokens = []
    palabras_vacias = stopwords.words('spanish')
    tokenizador = ToktokTokenizer()
    tokens_pos = tokenizador.tokenize(frases_pos)
    tokens_neg = tokenizador.tokenize(frases_neg)
    
    tokens.extend([t for t in tokens_pos if t not in palabras_vacias])
    tokens.extend([t for t in tokens_neg if t not in palabras_vacias])

    return tokens

def buscar_palabras(dataset, palabras_dataset):
    tokenizador = ToktokTokenizer()
    palabras = tokenizador.tokenize(dataset)
    datos = {}

    for p in palabras_dataset:
        datos[p] = (p in palabras)

    return datos

def entrenar_clasificador(dataset_entretamiento):
    clasificador = nltk.NaiveBayesClassifier.train(dataset_entretamiento)
    clasificador_archivo = open("clasificador.pickle","wb")
    pickle.dump(clasificador, clasificador_archivo)
    clasificador_archivo.close()
    return clasificador

def cargar_clasificador():
    clasificador_archivo = open("clasificador.pickle", "rb")
    clasificador = pickle.load(clasificador_archivo)
    clasificador_archivo.close()

    return clasificador

def clasificar(texto, clasificador, palabras_dataset):
    datos = buscar_palabras(texto, palabras_dataset)
    return clasificador.classify(datos)

if __name__ == "__main__":
    frases_pos = leer_archivo("pos.txt")
    frases_neg = leer_archivo("neg.txt")

    frases_dataset = etiquetar_datos(frases_pos, frases_neg)
    frases_token = tokenizar_dataset(frases_pos, frases_neg)
    frases_token = nltk.FreqDist(frases_token)

    palabras_dataset = list(frases_token.keys())[:3000]
    dataset = [(buscar_palabras(palabra, palabras_dataset), categoria) for (palabra, categoria) in frases_dataset]
    dataset_entretamiento = dataset[:1900]
    dataset_pruebas =  dataset[1900:]

    # clasificador = entrenar_clasificador(dataset_entretamiento)
    clasificador = cargar_clasificador()

    clasificador.show_most_informative_features(15)
    print("Precisión del clasificador Naive Bayes:", (nltk.classify.accuracy(clasificador, dataset_pruebas))*100)

    texto1 = "Muchas gracias por el regalo, fue un excelente detalle"
    texto2 = "Este clima está horrible, detesto cuando llueve"
    print(texto1, ":", clasificar(texto1, clasificador, palabras_dataset))
    print(texto2, ":", clasificar(texto2, clasificador, palabras_dataset))

    tiempo_fin = time.time()

    print("Tiempo de ejecución: ", tiempo_fin-tiempo_inicio)