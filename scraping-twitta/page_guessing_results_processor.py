from csv import DictReader
from re import search
from sys import argv


# Variable global que almacena el número de páginas real a adivinar
# Se inicializa en 0 y se modifica en la función principal
# La hacemos global para poder acceder a ella desde las funciones que la requieran sin necesidad de pasarla como argumento
# Esto simplifica sus firmas y es útil para funciones anidadas, pero no es algo de lo que abusar
pages_count = 0


# Función que extrae los resultados del archivo CSV generado por el scraper a un diccionario de Python
def get_results_dict(dictReader):
    # Inicializamos el diccionario donde se almacenarán los datos de interés de los tweets recolectados en el archivo CSV
    results = {}

    # dictReader es un objeto que permite iterar sobre las filas del archivo CSV para generar las entradas del diccionario
    for row in dictReader:
        # Inicializamos el diccionario donde se almacenarán los resultados de la fila actual
        results_row = {}
        message = row["Content"]
        # Se busca un número en el texto del mensaje
        number_match = search(r'[\d]+', message)
        
        # Si no se encuentra un número, se salta la entrada (tweet)
        if not number_match:
            continue

        # Se crea una entrada del diccionario con el número de páginas adivinado, el mensaje y la fecha
        timestamp = row["Timestamp"]
        results_row["guess"] = int(number_match.group())
        results_row["message"] = message
        results_row["timestamp"] = timestamp

        # Se añade la entrada al diccionario de resultados
        # La clave es una tupla con el nombre de usuario ("handle") y la fecha del tweet
        results[(row["Handle"], timestamp)] = results_row

    return results


# Función que define el criterio de ordenamiento de los resultados
# Se ordena por la diferencia entre el número adivinado y el número real de páginas
# item es una tupla (clave, valor) del diccionario de resultados, por lo que item[1] es el valor en el diccionario
def sorting_function(item):
    return abs(item[1]["guess"] - pages_count)


# Función que ordena los resultados por el criterio definido en sorting_function
# El diccionario de resultados se transforma en una lista de tuplas (clave, valor)
# Luego se ordena esta lista con el criterio anterior y se vuelve a convertir en un diccionario
# Nota: se requiere Python 3.7+ para mantener el orden de inserción en los diccionarios
def sort_results_by_guess(results):
    return {k: v for k, v in 
            sorted(results.items(), 
                   key=sorting_function)}


# Función que formatea los resultados para mostrarlos por pantalla
# Se toman únicamente las primeras 5 entradas del diccionario de resultados ordenado
# k[0] es el nombre de usuario y v es el valor asociado con el número adivinado, el mensaje y la fecha
def format_results(results):
    return "\n".join(
        [f"{k[0]}: {v['guess']} - ({v['message']} [{v['timestamp']}])" 
         for k, v in list(results.items())[:5]])


# Función principal que procesa los resultados del scraper y los muestra por pantalla
def main():
    global pages_count
    if len(argv) != 3:
        print("Usage: python page_guessing_results.py <pages_count> <results_csv>")
        return

    # Se obtiene el número de páginas real a adivinar y el archivo CSV con los resultados por línea de comandos
    pages_count = int(argv[1])
    dictReader = DictReader(open(argv[2], "r", encoding="utf-8"))

    # De dentro hacia afuera: se obtienen los resultados, se ordenan, se formatean y se imprimen por pantalla
    print(
        format_results(
            sort_results_by_guess(
                get_results_dict(dictReader))))


# Se llama a la función principal cuando se ejecuta el script directamente
if __name__ == "__main__":
    main()