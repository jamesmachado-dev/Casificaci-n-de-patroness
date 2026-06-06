import tkinter as tk
from tkinter import ttk

# 1. Base de datos de ejemplos (Imágenes binarias de 3x3 como ejemplo)
# 1 representa píxel activo (negro/blanco) y 0 inactivo
ejemplos = {
    "Positivo 1 (T normal)": [1, 1, 1, 
                              0, 1, 0, 
                              0, 1, 0],
    "Positivo 2 (T pequeña)": [0, 0, 0, 
                               1, 1, 1, 
                               0, 1, 0],
    "Negativo 1 (Línea)":    [1, 1, 1, 
                              0, 0, 0, 
                              0, 0, 0],
    "Negativo 2 (Vacío)":    [0, 0, 0, 
                              0, 0, 0, 
                              0, 0, 0]
}

# Inicializamos 9 pesos aleatorios/básicos para una matriz de 3x3
pesos = [1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0]
threshold = 2.0

def calcular_clasificacion():
    global threshold
    # Obtener el ejemplo seleccionado
    ejemplo_nombre = combo_ejemplos.get()
    imagen = ejemplos[ejemplo_nombre]
    
    # CALCULAR EL PUNTAJE (score = suma de pixel * peso)
    score = sum(p * w for p, w in zip(imagen, pesos))
    
    # REGLA DE CLASIFICACIÓN (Basado en image_493fef.png)
    if score > threshold:
        decision = "Es una T"
        color_resultado = "green"
    else:
        decision = "No es una T"
        color_resultado = "red"
        
    # Actualizar Interfaz
    lbl_score.config(text=f"Puntaje: {score:.2f}")
    lbl_threshold_val.config(text=f"Threshold Actual: {threshold:.2f}")
    lbl_decision.config(text=f"Decisión: {decision}", foreground=color_resultado)

def actualizar_threshold(val):
    global threshold
    threshold = float(val)
    calcular_clasificacion()

def actualizar_peso(index, val):
    pesos[index] = float(val)
    calcular_clasificacion()

# --- Configuración de la Ventana Principal (Tkinter) ---
root = tk.Tk()
root.title("Tarea 3 — Clasificando Patrones con una Máquina Simple")
root.geometry("500x500")

# Selector de ejemplos
tk.Label(root, text="Selecciona un Ejemplo:", font=('Arial', 12, 'bold')).pack(pady=5)
combo_ejemplos = ttk.Combobox(root, values=list(ejemplos.keys()), state="readonly")
combo_ejemplos.current(0)
combo_ejemplos.pack()
combo_ejemplos.bind("<<ComboboxSelected>>", lambda e: calcular_clasificacion())

# Slider para el Threshold
tk.Label(root, text="Modificar Threshold:", font=('Arial', 10, 'bold')).pack(pady=10)
slider_threshold = ttk.Scale(root, from_=-5, to=5, value=threshold, orient="horizontal", command=actualizar_threshold)
slider_threshold.pack(fill="x", padx=20)

# Sliders para los Pesos (Sección interactiva)
tk.Label(root, text="Modificar Pesos (Matriz 3x3):", font=('Arial', 10, 'bold')).pack(pady=10)
frame_pesos = tk.Frame(root)
frame_pesos.pack()

# Creamos una cuadrícula de sliders para simular los píxeles
for i in range(9):
    r, c = i // 3, i % 3
    sub_frame = tk.Frame(frame_pesos)
    sub_frame.grid(row=r, column=c, padx=5, pady=5)
    tk.Label(sub_frame, text=f"W{i+1}").pack()
    s = ttk.Scale(sub_frame, from_=-2, to=2, value=pesos[i], orient="vertical", command=lambda val, idx=i: actualizar_peso(idx, val))
    s.pack()

# --- Resultados (Requisitos Mínimos) ---
tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

lbl_score = tk.Label(root, text="Puntaje: 0.0", font=('Arial', 11))
lbl_score.pack()

lbl_threshold_val = tk.Label(root, text=f"Threshold Actual: {threshold}", font=('Arial', 11))
lbl_threshold_val.pack()

lbl_decision = tk.Label(root, text="Decisión: -", font=('Arial', 14, 'bold'))
lbl_decision.pack(pady=10)

# Arrancar la app y evaluar el primer ejemplo
calcular_clasificacion()
root.mainloop().