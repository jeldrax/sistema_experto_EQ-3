import json

def eliminar_duplicados(archivo_entrada, archivo_salida):
    try:
        # 1. Cargar los datos
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        print(f"Total de hechos originales: {len(datos)}")
        
        # 2. Filtrar duplicados
        unicos = []
        vistos = set()
        
        for dato in datos:
            # Convertimos el diccionario a una "tupla" para poder compararlo fácilmente
            # (Usamos solo las preguntas clave para detectar duplicados, ignorando la imagen si quieres)
            identificador = (
                dato['Sabor'], 
                dato['Temperatura'], 
                dato['Intensidad'], 
                dato['Leche']
            )
            
            if identificador not in vistos:
                vistos.add(identificador)
                unicos.append(dato)
            else:
                print(f"⚠️ Duplicado encontrado y eliminado: {identificador}")

        print(f"Total de hechos únicos: {len(unicos)}")

        # 3. Guardar el archivo limpio
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(unicos, f, indent=2, ensure_ascii=False)
            
        print(f"¡Listo! Archivo limpio guardado en: {archivo_salida}")

    except Exception as e:
        print(f"Error: {e}")

# Ejecutar
eliminar_duplicados('conocimientos_bebidas.json', 'conocimientos_limpios.json')