import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import messagebox
import math
import re
import cmath # pour racines complexes

# Fonction pour convertir la fonction en notation LaTeX pour un affichage plus naturel
def to_latex(expr):
    expr = expr.replace("**", "^")  # Remplacer seulement les puissances
    return expr

# Fonction pour tracer la courbe
def plot_function():
    global func_str  # Rendre la fonction accessible à d'autres parties du code
    func_str = entry_func.get()  # Récupérer la fonction entrée par l'utilisateur
    x = np.linspace(-100, 100, 4000)  # Générer des valeurs pour x

    try:
        y = [eval(func_str, {"x": i, "np": np, "math": math}) for i in x]  # Évaluer la fonction

        latex_func = to_latex(func_str)

        for widget in graph_frame.winfo_children():  # Effacer les widgets précédents
            widget.destroy()

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(f"Courbe de la fonction: $f(x) = {latex_func}$", fontsize=14)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur dans l'expression : {e}")

# Fonction pour extraire les coefficients d'une fonction affine ou polynôme
def extraire_coefficients(func_str):
    # Format fonction affine (chatgpt)
    affine_pattern = r'([+-]?[\d]*\.?[\d]*)?\s*\*\s*x\s*([+-]?\s*[\d]*\.?[\d]*)?$'
    # Format polynome second degree (chatgpt)
    polynome_pattern = r'([+-]?[\d]*\.?[\d]*)?\s*\*\s*x\*\*2\s*([+-]?\s*[\d]*\.?[\d]*)?\s*\*\s*x\s*([+-]?\s*[\d]*\.?[\d]*)?$'

    cleaned_func_str = func_str.replace(" ", "")  # Nettoyer la chaîne

    match_affine = re.fullmatch(affine_pattern, cleaned_func_str)
    match_polynome = re.fullmatch(polynome_pattern, cleaned_func_str)

    if match_affine:
        a = float(match_affine.group(1)) if match_affine.group(1) not in ["", "+", "-"] else (1.0 if match_affine.group(1) in ["", "+"] else -1.0)
        b = float(match_affine.group(2)) if match_affine.group(2) and match_affine.group(2) not in ["+", "-"] else 0.0
        return "Affine", a, b

    elif match_polynome:
        a = float(match_polynome.group(1)) if match_polynome.group(1) not in ["", "+", "-"] else (1.0 if match_polynome.group(1) in ["", "+"] else -1.0)
        b = float(match_polynome.group(2).replace(" ", "")) if match_polynome.group(2) and match_polynome.group(2) not in ["+", "-"] else 0.0
        c = float(match_polynome.group(3).replace(" ", "")) if match_polynome.group(3) else 0.0
        return "Polynôme", a, b, c

    else:
        return None  # Fonction non reconnue

# Fonction pour calculer et afficher les données spécifiques à la fonction choisie
def calculer_donnees():
    coefficients = extraire_coefficients(func_str)

    if coefficients is None:
        messagebox.showerror("Erreur", "La fonction entrée n'est ni affine ni polynomiale.")
        return

    choix = coefficients[0]
    result_text = ""

    if choix == "Affine":
        a, b = coefficients[1], coefficients[2]
        pente = a
        racine = -b/a if a != 0 else None
        result_text = f"Pente : {pente}\n"
        result_text += f"Racine : {racine}" if racine is not None else "Pas de racine"

    elif choix == "Polynôme":
        a, b, c = coefficients[1], coefficients[2], coefficients[3]
        alpha = round((-b) / (2*a), 3)
        delta = round(b**2 - 4*a*c, 3)
        beta = round((-delta) / 4*a)
        if delta > 0:
            racine1 = round((-b - math.sqrt(delta)) / (2*a), 3)
            racine2 = round((-b + math.sqrt(delta)) / (2*a), 3)
            forme_factorisee = f"{a}(x-{racine1})(x-{racine2})"
            result_text = f"Delta = {delta}\nx1 = {racine1} et x2 = {racine2}"
        elif delta == 0:
            racine = alpha
            forme_factorisee = f"{a}(x-{racine})²"
            result_text = f"Delta = {delta}\nx0 = {racine}"
        else:
            racine1 = (-b - cmath.sqrt(delta)) / (2*a)
            racine2 = (-b + cmath.sqrt(delta)) / (2*a)
            forme_factorisee = f"{a}(x-{racine1})(x-{racine2})"
            result_text = f"Delta = {delta}\nx1 = {racine1} et x2 = {racine2}"
        
        forme_canonique = f"{a}(x-{alpha})+{beta}"
        result_text += f"\nAlpha = {alpha}\nBeta = {beta}\nForme canonique = {forme_canonique}\nForme factorisée = {forme_factorisee}"
    # Afficher le résultat
    result_label.config(text=result_text)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Graphique et calculateur de fonction")

# Frame pour l'entrée de fonction et le tracé
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, padx=10, pady=10)

label_func = tk.Label(control_frame, text="Entrez une fonction en x (ex: np.sin(x), x**2, etc.):")
label_func.pack(side=tk.LEFT, padx=10)

entry_func = tk.Entry(control_frame, width=40)
entry_func.pack(side=tk.LEFT, padx=10)

button_func = tk.Button(control_frame, text="Tracer la fonction", command=plot_function)
button_func.pack(side=tk.LEFT, padx=10)

# Frame pour afficher la courbe
graph_frame = tk.Frame(root)
graph_frame.pack(fill=tk.BOTH, expand=True)

# Frame pour les champs de paramètres
params_frame = tk.Frame(root)
params_frame.pack(padx=10, pady=10)

# Bouton pour calculer les données
btn_calculer = tk.Button(root, text="Calculer les données", command=calculer_donnees)
btn_calculer.pack(padx=10, pady=10)

# Label pour afficher les résultats
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack(padx=10, pady=10)

# Lancer la boucle principale de Tkinter
root.mainloop()
