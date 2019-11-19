from random import randint

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
    
def getTypeByIndex(myIndex):

    #types = ["Acero", "Agua", "Bicho", "Dragón", "Eléctrico", "Fantasma", "Fuego", "Hada", "Hielo", "Lucha", "Normal", "Planta", "Psíquico", "Roca", "Siniestro", "Tierra", "Veneno", "Volador"]
    return types[myIndex]

def getIndexByType(myType):

    #types = ["Acero", "Agua", "Bicho", "Dragón", "Eléctrico", "Fantasma", "Fuego", "Hada", "Hielo", "Lucha", "Normal", "Planta", "Psíquico", "Roca", "Siniestro", "Tierra", "Veneno", "Volador"]
    return types.index(myType)

def getEffectiveness(attacker, defender):
    return tablaEfectividades[attacker][defender]

def getEfectividadesByTipo(tipo):
    texto = "Las efectividades de " + tipo + " son:\n"
    indexTipo = getIndexByType(tipo)
    efectividadesAtacante = tablaEfectividades[indexTipo]
    
    cont = 0
    for efectividad in efectividadesAtacante:
        if efectividad != 1:
            defensor = getTypeByIndex(cont)
            texto += defensor + ": " + str(efectividad) + "\n"
        cont += 1
            
    return texto
    
def getTypes():
    texto = "Elige un tipo de Pokémon:\n"
    
    for type in types:
        texto += "<botontipo>/efectividades " + type + "\n"
    
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
    
def procesarRespuesta(texto):
    atacante = texto.split(" ")[0]
    defensor = texto.split(" ")[1]
    elegida = texto.split(" ")[2]

    efectividad = getEffectiveness(getIndexByType(atacante), getIndexByType(defensor))

    if str(efectividad) == str(elegida):
        return "Correcto!\n" + hacerPregunta()
    else:
        return "Error, la efectividad es " + str(efectividad) + "\n" + hacerPregunta()
