import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

# --- CONFIGURACIÓN ---
ARCHIVO_JSON = 'conocimientos_bebidas.json'
COLOR_FONDO = "#FDF5E6"
COLOR_ACCENTO = "#6F4E37"
COLOR_TEXTO = "#3E2723"

class SistemaExpertoBebidas:
    def __init__(self, root):
        self.root = root
        self.root.title("Barista Experto - Recomendador de Bebidas")
        self.root.geometry("1000x700") 
        self.root.configure(bg=COLOR_FONDO)

        # Variables para manejar múltiples resultados
        self.resultados_encontrados = []
        self.indice_actual = 0

        self.opciones_sabor = [
            "Prefiero las bebidas con un toque dulce.",
            "Me gustan más con sabor amargo"
        ]
        self.opciones_temperatura = [
            "Me gusta que esté fría, algo refrescante.",
            "Prefiero que esté templada, ni muy fría ni muy caliente.",
            "La quiero caliente, como café recién hecho."
        ]
        self.opciones_intensidad = [
            "Me gustan las bebidas suaves, casi sin sabor fuerte.",
            "Prefiero un sabor intermedio, equilibrado.",
            "Me gustan las bebidas muy intensas, con sabor marcado"
        ]
        self.opciones_leche = [
            "Me gustaría que tenga leche de almendra.",
            "Prefiero que sea deslactosada.",
            "Me gusta con leche entera.",
            "No quiero leche en mi bebida."
        ]

        # --- CAMBIO AQUÍ: Lógica de Bienvenida ---
        self.root.withdraw()      # 1. Ocultar la ventana principal
        self.mostrar_bienvenida() # 2. Mostrar la bienvenida
        self.root.deiconify()     # 4. Mostrar la ventana principal (al cerrar bienvenida)
        self.crear_interfaz()     # 5. Cargar la interfaz

    def mostrar_bienvenida(self):
        """Muestra una ventana de bienvenida antes de iniciar."""
        vent_bienvenida = tk.Toplevel(self.root)
        vent_bienvenida.title("Bienvenido")
        vent_bienvenida.geometry("500x400")
        vent_bienvenida.configure(bg=COLOR_FONDO)
        
        # Centrar la ventana (opcional, pero se ve mejor)
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        vent_bienvenida.geometry(f"500x400+{x}+{y}")

        # Contenido
        tk.Label(vent_bienvenida, text="☕", font=("Arial", 60), bg=COLOR_FONDO).pack(pady=(30, 8))
        
        tk.Label(vent_bienvenida, text="¡Bienvenido a\nBarista Experto!", 
                 font=("Helvetica", 24, "bold"), fg=COLOR_ACCENTO, bg=COLOR_FONDO, justify="center").pack(pady=10)

        tk.Label(vent_bienvenida, text="Encuentra tu bebida ideal respondiendo\nunas sencillas preguntas.", 
                 font=("Arial", 12), fg=COLOR_TEXTO, bg=COLOR_FONDO, justify="center").pack(pady=10)

        # Botón para cerrar y continuar
        tk.Button(vent_bienvenida, text="COMENZAR", bg=COLOR_ACCENTO, fg="white", 
                  font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2",
                  command=vent_bienvenida.destroy).pack(pady=40)

        # 3. Esperar aquí hasta que se cierre esta ventana
        self.root.wait_window(vent_bienvenida)

    def cargar_datos(self):
        if not os.path.exists(ARCHIVO_JSON):
            return []
        try:
            with open(ARCHIVO_JSON, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except:
            return []

    def guardar_datos(self, nuevo_dato):
        datos = self.cargar_datos()
        datos.append(nuevo_dato)
        with open(ARCHIVO_JSON, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def crear_interfaz(self):
        # Frame Izquierdo
        frame_izq = tk.Frame(self.root, bg=COLOR_FONDO, padx=30, pady=30)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(frame_izq, text="Barista virtual", font=("Helvetica", 18, "bold"), fg=COLOR_ACCENTO, bg=COLOR_FONDO).pack(anchor="w", pady=(0, 30))

        # Preguntas
        tk.Label(frame_izq, text="¿Qué tipo de sabor prefieres?", font=("Arial", 11, "bold"), bg=COLOR_FONDO).pack(anchor="w", pady=(10, 5))
        self.combo_sabor = ttk.Combobox(frame_izq, values=self.opciones_sabor, width=50, state="readonly")
        self.combo_sabor.pack(anchor="w")

        tk.Label(frame_izq, text="¿Cómo prefieres la temperatura?", font=("Arial", 11, "bold"), bg=COLOR_FONDO).pack(anchor="w", pady=(10, 5))
        self.combo_temp = ttk.Combobox(frame_izq, values=self.opciones_temperatura, width=50, state="readonly")
        self.combo_temp.pack(anchor="w")

        tk.Label(frame_izq, text="¿Qué tan intensa te gusta tu bebida?", font=("Arial", 11, "bold"), bg=COLOR_FONDO).pack(anchor="w", pady=(10, 5))
        self.combo_int = ttk.Combobox(frame_izq, values=self.opciones_intensidad, width=50, state="readonly")
        self.combo_int.pack(anchor="w")

        tk.Label(frame_izq, text="¿Qué tipo de leche prefieres?", font=("Arial", 11, "bold"), bg=COLOR_FONDO).pack(anchor="w", pady=(10, 5))
        self.combo_leche = ttk.Combobox(frame_izq, values=self.opciones_leche, width=50, state="readonly")
        self.combo_leche.pack(anchor="w")

        # Botones Principales
        frame_btn = tk.Frame(frame_izq, bg=COLOR_FONDO)
        frame_btn.pack(pady=30, anchor="w")
        
        tk.Button(frame_btn, text="RECOMENDAR BEBIDA", bg=COLOR_ACCENTO, fg="white", font=("Arial", 11, "bold"), padx=15, pady=5, command=self.consultar).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(frame_btn, text="LIMPIAR", bg="#D7CCC8", fg=COLOR_TEXTO, font=("Arial", 11), padx=15, pady=5, command=self.limpiar).pack(side=tk.LEFT)


        # Frame Derecho
        frame_der = tk.Frame(self.root, bg="white", padx=30, pady=30, relief="raised", borderwidth=1)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame_der, text="RECOMENDACIÓN", font=("Helvetica", 16, "bold"), fg=COLOR_ACCENTO, bg="white").pack(pady=(10, 5))
        
        # Etiqueta para mostrar "Resultado 1 de 2"
        self.lbl_contador = tk.Label(frame_der, text="", font=("Arial", 10), fg="gray", bg="white")
        self.lbl_contador.pack()

        # Resultado
        self.lbl_resultado = tk.Label(frame_der, text="...", font=("Arial", 14, "bold"), fg=COLOR_TEXTO, bg="white", wraplength=350)
        self.lbl_resultado.pack(pady=10)

        # Imagen
        self.lbl_imagen = tk.Label(frame_der, bg="white")
        self.lbl_imagen.pack(pady=10)

        # Botones de Navegación
        self.frame_nav = tk.Frame(frame_der, bg="white")
        self.frame_nav.pack(pady=5)
        
        self.btn_anterior = tk.Button(self.frame_nav, text="< Anterior", state="disabled", command=self.mostrar_anterior)
        self.btn_anterior.pack(side=tk.LEFT, padx=10)
        
        self.btn_siguiente = tk.Button(self.frame_nav, text="Siguiente >", state="disabled", command=self.mostrar_siguiente)
        self.btn_siguiente.pack(side=tk.LEFT, padx=10)

        self.btn_explicacion = tk.Button(frame_der, text="¿Por qué esta bebida?", state="disabled", command=self.mostrar_explicacion)
        self.btn_explicacion.pack(pady=10)
        
        self.lbl_explicacion = tk.Label(frame_der, text="", font=("Arial", 10, "italic"), fg="#5D4037", bg="white", wraplength=350)
        self.lbl_explicacion.pack(pady=5)

    def consultar(self):
        sabor = self.combo_sabor.get()
        temp = self.combo_temp.get()
        intensidad = self.combo_int.get()
        leche = self.combo_leche.get()

        if not (sabor and temp and intensidad and leche):
            messagebox.showwarning("Faltan datos", "Por favor selecciona todas las opciones.")
            return

        conocimiento = self.cargar_datos()

        self.resultados_encontrados = []
        
        for regla in conocimiento:
            if (regla["Sabor"] == sabor and 
                regla["Temperatura"] == temp and 
                regla["Intensidad"] == intensidad and 
                regla["Leche"] == leche):
                
                self.resultados_encontrados.append(regla) 
        
        if len(self.resultados_encontrados) > 0:
            self.indice_actual = 0
            self.mostrar_resultado_actual()
        else:
            respuesta = messagebox.askyesno("Sin conocimiento", "No sé qué bebida recomendar para esa combinación exacta.\n\n¿Quieres enseñarme?")
            if respuesta:
                self.abrir_aprendizaje(sabor, temp, intensidad, leche)

    def mostrar_resultado_actual(self):
        regla = self.resultados_encontrados[self.indice_actual]
        total = len(self.resultados_encontrados)

        self.lbl_resultado.config(text=regla["Diagnostico"])
        self.explicacion_pendiente = regla["Explicacion"]
        self.lbl_explicacion.config(text="") 
        self.btn_explicacion.config(state="normal")
        
        if total > 1:
            self.lbl_contador.config(text=f"Resultado {self.indice_actual + 1} de {total}")
        else:
            self.lbl_contador.config(text="")

        if total > 1:
            self.btn_anterior.config(state="normal" if self.indice_actual > 0 else "disabled")
            self.btn_siguiente.config(state="normal" if self.indice_actual < total - 1 else "disabled")
        else:
            self.btn_anterior.config(state="disabled")
            self.btn_siguiente.config(state="disabled")

        try:
            if os.path.exists(regla["Imagen"]):
                img = Image.open(regla["Imagen"])
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.lbl_imagen.config(image=photo)
                self.lbl_imagen.image = photo
            else:
                self.lbl_imagen.config(image='', text="(Imagen no disponible)")
        except:
            self.lbl_imagen.config(image='', text="(Error de imagen)")

    def mostrar_siguiente(self):
        if self.indice_actual < len(self.resultados_encontrados) - 1:
            self.indice_actual += 1
            self.mostrar_resultado_actual()

    def mostrar_anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_resultado_actual()

    def mostrar_explicacion(self):
        self.lbl_explicacion.config(text=self.explicacion_pendiente)

    def limpiar(self):
        self.combo_sabor.set('')
        self.combo_temp.set('')
        self.combo_int.set('')
        self.combo_leche.set('')
        self.lbl_resultado.config(text="...")
        self.lbl_imagen.config(image='', text="")
        self.lbl_explicacion.config(text="")
        self.lbl_contador.config(text="")
        self.btn_explicacion.config(state="disabled")
        self.btn_anterior.config(state="disabled")
        self.btn_siguiente.config(state="disabled")

    def abrir_aprendizaje(self, s, t, i, l):
        vent = tk.Toplevel(self.root)
        vent.title("Módulo de Aprendizaje")
        vent.geometry("400x450")
        vent.configure(bg=COLOR_FONDO)

        tk.Label(vent, text="Enséñame una nueva bebida", font=("Arial", 12, "bold"), bg=COLOR_FONDO).pack(pady=10)
        
        tk.Label(vent, text="Nombre de la bebida recomendada:", bg=COLOR_FONDO).pack(anchor="w", padx=20)
        entry_diag = tk.Entry(vent, width=40)
        entry_diag.pack(padx=20, pady=5)

        tk.Label(vent, text="Explicación (¿Por qué?):", bg=COLOR_FONDO).pack(anchor="w", padx=20)
        entry_exp = tk.Entry(vent, width=40)
        entry_exp.pack(padx=20, pady=5)

        tk.Label(vent, text="Nombre de archivo de imagen (ej: late.jpg):", bg=COLOR_FONDO).pack(anchor="w", padx=20)
        entry_img = tk.Entry(vent, width=40)
        entry_img.pack(padx=20, pady=5)

        def guardar():
            nuevo = {
                "Sabor": s,
                "Temperatura": t,
                "Intensidad": i,
                "Leche": l,
                "Diagnostico": entry_diag.get(),
                "Explicacion": entry_exp.get(),
                "Imagen": entry_img.get()
            }
            self.guardar_datos(nuevo)
            messagebox.showinfo("Éxito", "¡Gracias! Ahora soy más experto.")
            vent.destroy()
            self.consultar()

        tk.Button(vent, text="GUARDAR CONOCIMIENTO", bg=COLOR_ACCENTO, fg="white", command=guardar).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoBebidas(root)
    root.mainloop()