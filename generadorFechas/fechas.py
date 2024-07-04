from datetime import datetime, timedelta

def generar_fechas(num_fechas, fechas_por_dia, fecha_inicio_str):
    # Convertir la fecha de inicio a un objeto datetime
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    
    # Calcular el intervalo entre fechas
    intervalo = timedelta(days=1 / fechas_por_dia)
    
    # Crear la lista de fechas
    lista_fechas = []
    for i in range(num_fechas):
        nueva_fecha = fecha_inicio + i * intervalo
        lista_fechas.append(nueva_fecha.strftime("%Y-%m-%d %H:%M:%S"))
    
    return lista_fechas

# Ejemplo de uso
num_fechas = 120
fechas_por_dia = 5
fecha_inicio_str = "2024-07-05 00:00:00"

fechas_generadas = generar_fechas(num_fechas, fechas_por_dia, fecha_inicio_str)
for fecha in fechas_generadas:
    print(fecha)
