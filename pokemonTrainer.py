from random import randint
from pokemonTrainerPersistance import *

types = ["Acero", "Agua", "Bicho", "Dragón", "Eléctrico", "Fantasma", "Fuego", "Hada", "Hielo", "Lucha", "Normal", "Planta", "Psíquico", "Roca", "Siniestro", "Tierra", "Veneno", "Volador"]
tablaEfectividades =[
    [0.5, 0.5, 1, 1, 0.5, 1, 0.5, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [1, 0.5, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 1, 1],
    [0.5, 1, 1, 1, 1, 0.5, 0.5, 0.5, 1, 0.5, 1, 2, 2, 1, 2, 1, 0.5, 0.5],
    [0.5, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 1, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 0, 1, 2],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 2, 1, 0.5, 1, 1, 1],
    [2, 0.5, 2, 0.5, 1, 1, 0.5, 1, 2, 1, 1, 2, 1, 0.5, 1, 1, 1, 1],
    [0.5, 1, 1, 2, 1, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 2, 1, 0.5, 1],
    [0.5, 0.5, 1, 2, 1, 1, 0.5, 1, 0.5, 1, 1, 2, 1, 1, 1, 2, 1, 2],
    [2, 1, 0.5, 1, 1, 0, 1, 0.5, 2, 1, 2, 1, 0.5, 2, 2, 1, 0.5, 0.5],
    [0.5, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1],
    [0.5, 2, 0.5, 0.5, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 2, 1, 2, 0.5, 0.5],
    [0.5, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 1, 0, 1, 2, 1],
    [0.5, 1, 2, 1, 1, 1, 2, 1, 2, 0.5, 1, 1, 1, 1, 1, 0.5, 1, 2],
    [1, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 1, 1, 2, 1, 0.5, 1, 1, 1],
    [2, 1, 0.5, 1, 2, 1, 2, 1, 1, 1, 1, 0.5, 1, 2, 1, 1, 2, 0],
    [0, 1, 1, 1, 1, 0.5, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 1],
    [0.5, 1, 2, 1, 0.5, 1, 1, 1, 1, 2, 1, 2, 1, 0.5, 1, 1, 1, 1]
]

def get_stats(chat_id):
    text = "Estadísticas de aciertos:\n"
    stats = get_stats_from_db(chat_id)
    cont = -1
    
    for stat in stats.replace(" ", "").replace("(", "").replace(")","").split(","):
        if cont == -1:
            pass
        else:
            text += getTypeByIndex(cont) + ": " + stat + "\n"
        cont +=1
    
    return text
    
def reset_stats(chat_id):
    delete_my_stats(chat_id)
    return "Stats reseted"

def getTypeByIndex(myIndex):
    return types[myIndex]

def getIndexByType(myType):

    #types = ["Acero", "Agua", "Bicho", "Dragón", "Eléctrico", "Fantasma", "Fuego", "Hada", "Hielo", "Lucha", "Normal", "Planta", "Psíquico", "Roca", "Siniestro", "Tierra", "Veneno", "Volador"]
    return types.index(myType)

def getEffectiveness(attacker, defender):
    return tablaEfectividades[attacker][defender]

def getEfectividadesByTipo(tipo, rol):
    texto = "Las efectividades de " + tipo + " como " + rol + " son:\n"
    indexTipo = getIndexByType(tipo)
    if "atacante" in rol:
        efectividades = tablaEfectividades[indexTipo]
    if "defensor" in rol:
        efectividades = []
        for index in range(0, len(types)-1):
            efectividades.append(tablaEfectividades[index][indexTipo])
    
    cont = 0
    for efectividad in efectividades:
        if efectividad != 1:
            defensor = getTypeByIndex(cont)
            texto += defensor + ": " + str(efectividad) + "\n"
        cont += 1
            
    return texto
    
def getTypes(rol):
    texto = "Elige un tipo de Pokémon:\n"
    
    for type in types:
        texto += "<botontipo>/efectividades " + type + rol + "\n"
    
    return texto
        
def getRandomType():
    return getTypeByIndex(randint(0, 17))

def hacerPregunta():
    return textoPregunta(crearPregunta())

def crearPregunta():
    atacante = getRandomType()
    defensor = getRandomType()

    pregunta = {"Atacante" : atacante,
                "Defensor" : defensor,
                "Opciones" : [0, 0.5, 1, 2]
    }

    return pregunta
                

def textoPregunta(pregunta):
    texto = ""

    texto += pregunta["Atacante"] + " ataca a " + pregunta["Defensor"] + ". ¿Cuál es la efectividad?:\n"
    
    for opcion in pregunta["Opciones"]:
        texto += '<botonefectividad>/evaluar '
        texto += pregunta["Atacante"] + ' '
        texto += pregunta["Defensor"] + ' '
        texto += str(opcion) + "\n"

    return texto
    
def procesarRespuesta(texto, my_chatid):
    atacante = texto.split(" ")[0]
    defensor = texto.split(" ")[1]
    elegida = texto.split(" ")[2]

    efectividad = getEffectiveness(getIndexByType(atacante), getIndexByType(defensor))

    if str(efectividad) == str(elegida):
        update_stats(my_chatid, atacante, defensor, "right")
        return "Correcto!\n" + hacerPregunta()
    else:
        update_stats(my_chatid, atacante, defensor, "wrong")
        return "Error, la efectividad es " + str(efectividad) + "\n" + hacerPregunta()
