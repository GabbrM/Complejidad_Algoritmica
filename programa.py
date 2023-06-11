import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import csv
from tkinter import ttk

# Lista de películas recomendadas (título, imagen)
peliculas = []

# Cargar datos del archivo CSV
with open('peliculas.csv', 'r', encoding='utf-8') as archivo_csv:
    lector_csv = csv.reader(archivo_csv, delimiter=';')
    for fila in lector_csv:
        titulo = fila[0]
        imagen = fila[-1]
        peliculas.append({'Title': titulo, 'Image': imagen})

def cambiar_pelicula(event):
    titulo_seleccionado = combobox_peliculas.get()

    for pelicula in peliculas:
        if pelicula['Title'] == titulo_seleccionado:
            imagen_ruta = pelicula['Image']
            imagen = Image.open(imagen_ruta)
            imagen = imagen.resize((400, 600), Image.ANTIALIAS)
            imagen = ImageTk.PhotoImage(imagen)
            imagen_principal_label.config(image=imagen)
            imagen_principal_label.image = imagen
            break

def mostrar_resultados(resultados):
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados de la búsqueda")

    if not resultados:
        mensaje_label = tk.Label(ventana_resultados, text="No se encontraron resultados")
        mensaje_label.pack(padx=20, pady=20)
    else:
        fila_actual = 0
        marco_fila = None

        for i, pelicula in enumerate(resultados):
            titulo = pelicula['Title']
            imagen_ruta = pelicula['Image']
            imagen = Image.open(imagen_ruta)
            imagen = imagen.resize((100, 150), Image.ANTIALIAS)
            imagen = ImageTk.PhotoImage(imagen)

            if i % 5 == 0:
                fila_actual += 1
                marco_fila = tk.Frame(ventana_resultados)
                marco_fila.pack(pady=10)

            marco_pelicula = tk.Frame(marco_fila)
            marco_pelicula.pack(side="left", padx=10)

            imagen_label = tk.Label(marco_pelicula, image=imagen)
            imagen_label.image = imagen  # Guardamos una referencia para evitar que se pierda la imagen
            imagen_label.pack()

            titulo_label = tk.Label(marco_pelicula, text=titulo)
            titulo_label.pack()

def buscar_pelicula():
    termino_busqueda = entrada_busqueda.get()

    resultados = []
    for pelicula in peliculas:
        if termino_busqueda.lower() in pelicula['Title'].lower():
            resultados.append(pelicula)

    mostrar_resultados(resultados)

def abrir_ventana_recomendaciones():
    ventana.withdraw()  # Ocultar la ventana principal

    # Crear una nueva ventana para las recomendaciones
    ventana_recomendaciones = tk.Toplevel()
    ventana_recomendaciones.title("Recomendaciones")
    texto_recomendaciones = tk.Label(ventana_recomendaciones, text="Ingresa o selecciona tu película favorita")
    texto_recomendaciones.pack()

    # Opciones de películas para el combobox
    opciones_peliculas = [pelicula['Title'] for pelicula in peliculas]

    # Combobox para seleccionar la película favorita
    combobox_pelicula_favorita = ttk.Combobox(ventana_recomendaciones, values=opciones_peliculas, width=50)
    combobox_pelicula_favorita.pack()

    def obtener_recomendaciones():
        pelicula_favorita = combobox_pelicula_favorita.get()

        #Implementar el algoritmo aquí

        # Mostrar las recomendaciones en una nueva ventana
        ventana_resultados = tk.Toplevel()
        ventana_resultados.title("Recomendaciones")

        # Puedes utilizar la función mostrar_resultados(resultados) para mostrar las películas recomendadas

    # Botón para obtener las recomendaciones
    boton_obtener_recomendaciones = tk.Button(ventana_recomendaciones, text="Obtener Recomendaciones", command=obtener_recomendaciones)
    boton_obtener_recomendaciones.pack(pady=10)

    def cerrar_ventana_recomendaciones():
        ventana_recomendaciones.destroy()  # Cerrar la ventana de recomendaciones
        ventana.deiconify()  # Mostrar nuevamente la ventana principal

    ventana_recomendaciones.protocol("WM_DELETE_WINDOW", cerrar_ventana_recomendaciones)

# Ventana principal
ventana = tk.Tk()
ventana.title("MovieMatch - Recomendación de películas")

# Contenedor principal
contenedor_principal = tk.Frame(ventana)
contenedor_principal.pack(fill=tk.BOTH, expand=True)

# Barra superior
barra_superior = tk.Frame(contenedor_principal, bg="black")
barra_superior.pack(fill=tk.X)

# Label del nombre del programa en la barra superior
label_titulo = tk.Label(barra_superior, text="MovieMatch", bg="black", fg="white", font=("Arial", 20))
label_titulo.pack(padx=400, pady=10, anchor="nw")

# Cuadro de texto de búsqueda en la barra superior
entrada_busqueda = tk.Entry(barra_superior, width=30)
entrada_busqueda.pack(padx=10, pady=5, side=tk.RIGHT)
boton_buscar = tk.Button(barra_superior, text="Buscar", command=buscar_pelicula)
boton_buscar.pack(padx=10, pady=5, side=tk.RIGHT)

# Color de fondo de la barra lateral
barra_lateral = tk.Frame(contenedor_principal, bg="black", width=200)
barra_lateral.pack(side=tk.LEFT, fill=tk.Y)

# Opciones de navegación en la barra lateral
opciones = ["Inicio", "Recomendaciones", "Recientes", "About the team"]
for opcion in opciones:
    if opcion == "Recomendaciones":
        boton = tk.Button(barra_lateral, text=opcion, bg="black", fg="white", bd=0, padx=10, pady=5, command=abrir_ventana_recomendaciones)
    else:
        boton = tk.Button(barra_lateral, text=opcion, bg="black", fg="white", bd=0, padx=10, pady=5)
    boton.pack(side=tk.TOP, fill=tk.X)

# Contenido principal
contenido_principal = tk.Frame(contenedor_principal)
contenido_principal.pack(fill=tk.BOTH, expand=True)

# Marco para la imagen principal en el contenido principal
marco_principal = tk.Frame(contenido_principal)
marco_principal.pack(side=tk.TOP, pady=1)

# Cargar la imagen principal
imagen_principal = ImageTk.PhotoImage(Image.open("images/11.jpg"))
imagen_principal_label = tk.Label(marco_principal, image=imagen_principal)
imagen_principal_label.pack(side="left")

# Marco para el combobox de películas en el contenido principal
marco_combobox = tk.Frame(contenido_principal)
marco_combobox.pack(side=tk.TOP, pady=10)

# Combobox de películas
combobox_peliculas = ttk.Combobox(marco_combobox, width=50)
combobox_peliculas.pack(side="left")

# Agregar las películas al combobox
combobox_peliculas['values'] = [pelicula['Title'] for pelicula in peliculas]

# Agregar el evento para cambiar la película seleccionada
combobox_peliculas.bind("<<ComboboxSelected>>", cambiar_pelicula)

# Ejecutar la aplicación
ventana.mainloop()
