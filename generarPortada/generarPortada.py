import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import datetime
import textwrap
from slugify import slugify

'''
En este código se genera una imagen de portada para un artículo de un blog de wordpress
con el título "Empresas de X en Yucatán" donde X es el tipo de la empresa que podría tener un directorio de empresas
y Yucatán es el estado de Yucatán. Se genera una imagen de portada por cada estado de México
y se guardan en la carpeta "generarPortada/portadas"

El código se puede adaptar a cualquier país o región, simplemente cambiando la lista de estados
y el texto que se va a generar en la imagen de portada.

También se puede adaptar para generar imágenes de portada para otros tipos de artículos, simplemente
cambiando el texto que se va a generar en la imagen de portada.

Para que el código funcione, se necesita una imagen de fondo que se va a usar para la portada. Se puede
descargar de internet, generar con openai o cualquier otra fuente. La imagen de fondo debe estar en la carpeta
"generarPortada" y se debe llamar "img.jpg" para que todo funcione sin tocar nada

El código también necesita una fuente para el texto que se va a generar en la imagen de portada. La fuente
debe estar en la carpeta "generarPortada" y se debe especificar en la variable "fontype" el nombre de la fuente
con la extensión .ttf o .otf

El código guarda las imágenes de portada en la carpeta "generarPortada/portadas" y genera una url para cada imagen
de portada que se puede usar en un CSV de importación a wordpress para importar las imágenes de portada de los artículos
de un blog.
'''


fontype = "generarPortada/jmh_typewriter_dry/JMH Typewriter dry.otf"
# puedes bajar las fuentes que quieras desde: https://www.dafont.com/es/
# recuerda que debes tener el archivo .ttf o .otf en la carpeta de tu proyecto
# ten en cuenta que si los títulos tienen acentos, debes usar una fuente que los tenga
# si no, los acentos no se verán en la imagen y se verán caracteres raros
carpetaPortadas = "generarPortada/portadas" # carpeta donde se guardarán las portadas
# dominio de tu sitio web para generar la url de la imagen del 
# tipo: https://dominiodeprueba.com/wp-content/uploads/2021/08/empresas-de-x-en-yucatan.webp
# para que puedas incluirlo en tu CSV de importación a wordpress como imagen de portada
dominio = "dominiodeprueba.com" 

estados_mexico = [
    "Aguascalientes",
    "Baja California",
    "Baja California Sur",
    "Campeche",
    "Chiapas",
    "Chihuahua",
    "Ciudad de México",
    "Coahuila",
    "Colima",
    "Durango",
    "Guanajuato",
    "Guerrero",
    "Hidalgo",
    "Jalisco",
    "México",
    "Michoacán",
    "Morelos",
    "Nayarit",
    "Nuevo León",
    "Oaxaca",
    "Puebla",
    "Querétaro",
    "Quintana Roo",
    "San Luis Potosí",
    "Sinaloa",
    "Sonora",
    "Tabasco",
    "Tamaulipas",
    "Tlaxcala",
    "Veracruz",
    "Yucatán",
    "Zacatecas"
]

#for estado in estados_mexico:
#    print(get_portada(estado, "generarPortada/img.jpg"))

def draw_centered_text(image, text, font, color=(255, 255, 255)):
    """
    Draws centered text on the given image.

    Args:
        image (PIL.Image.Image): The image to draw the text on.
        text (str): The text to be drawn.
        font (PIL.ImageFont.FreeTypeFont): The font to be used for the text.
        color (tuple, optional): The color of the text. Defaults to (255, 255, 255).

    Returns:
        PIL.Image.Image: The image with the centered text drawn on it.
    """
     # Crea un objeto Draw para poder dibujar en la imagen
    draw = ImageDraw.Draw(image)

    # Obtiene el ancho y el alto de la imagen
    width, height = image.size

    # Obtiene el ancho y el alto de un carácter para calcular cuántos caracteres caben en una línea
    char_width, char_height = font.getsize('A')  # Asume que todos los caracteres tienen el mismo tamaño

    # Calcula el número de caracteres que caben en una línea
    chars_per_line = width // char_width

    # Divide el texto en líneas de manera que cada línea tenga como máximo chars_per_line caracteres
    lines = textwrap.wrap(text, width=chars_per_line)

    # Calcula la posición y inicial para el texto de manera que el texto esté centrado verticalmente
    y_text = (height - char_height * len(lines)) / 2

    # Para cada línea de texto
    for line in lines:
        # Obtiene el ancho y el alto de la línea
        line_width, line_height = font.getsize(line)

        # Calcula la posición x para la línea de manera que la línea esté centrada horizontalmente
        x = (width - line_width) / 2

        # Dibuja la línea en la imagen
        draw.text((x, y_text), line, font=font, fill=color)

        # Incrementa y_text por el alto de la línea para la siguiente línea
        y_text += line_height

    # Devuelve la imagen con el texto dibujado
    return image

# datos para generar la url de la imagen de portada
today = datetime.date.today()
mes = today.month
y = today.year

# Uso de la función
imagen = Image.open("generarPortada/img.jpg")
font = ImageFont.truetype(fontype, 90)

for estado in estados_mexico:
    text = f"Empresas de X en {estado}"
    imagen = Image.open("generarPortada/img.jpg")
    imagen = draw_centered_text(imagen, text, font)
    imagen.save(os.path.join(carpetaPortadas, slugify(text)+".webp"), "WEBP", quality=20)
    # genera la url de la imagen de portada
    print (dominio + "/wp-content/uploads/"+str(y)+"/"+ "{:02d}".format(mes) + "/" +slugify(text) + ".webp")