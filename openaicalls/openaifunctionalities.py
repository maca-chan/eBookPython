import openai, time


# para que el código funcione, necesitas un archivo api.txt en la misma carpeta que este archivo
def chatGPT4o(prompt, tokens=2048):

    # nota: tienes dos variables: prompt e instrucciones
    # prompt es la pregunta que le haces a GPT-4o
    # instrucciones es la información que le pasas a GPT-4o para que genere una respuesta
    # por eso el prompt se pasa a esta función y las instrucciones se definen aquí mismo
    instrucciones = '''Aquí debes poner las instrucciones que quieras pasarle a GPT-4o para que genere una respuesta. Por ejemplo, si quieres que GPT-4o te diga cómo
    se hace una receta de cocina, puedes poner algo como: 'Escribe una receta de cocina para hacer pan de muerto'.'''


    with open('api.txt', 'r', encoding='utf-8') as f:
        apis = f.readlines()
        apis = [api.replace("\n","") for api in apis]
        openai.api_key = apis[0]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instrucciones},
                {"role": "user", "content": prompt}
            ],
            max_tokens=tokens,
            temperature=0.7
        )
        # print("\n\tPrompt:\n" + prompt)
        response = response.choices[0].message['content'].strip()
        # print("\n\tRespuesta:\n" + response)
        return response
    except Exception as error:
        # handle the exception
        print("Ha ocurrido un error: ", error)
        print("Reintentando...")
        time.sleep(0.5)
        openai.api_key = next(apis, openai.api_key) # pasamos a la siguiente api
        return chatGPT4o(prompt, tokens)

''' En esta función hacemos el cambio de la api_key en caso de que se haya agotado el límite de uso de la api_key actual.'''
def next(apis, api):
    # primero miramos cual es la longitud de la lista de apis
    l = len(apis)
    # luego buscamos la posición de la api actual en la lista de apis
    i = apis.index(api)
    # buscamos la siguiente api en la lista de apis
    # si llegamos al final de la lista, volvemos al principio (con la operación módulo)
    i = (i+1)%l
    # devolvemos la siguiente api
    return apis[i]