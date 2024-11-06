from flask import Flask, render_template, request
import numpy as np
from scipy.stats import f
from graficas import graficar_t2_con_limite, graficar_arl   

app = Flask(__name__)

def carta_control_t2(x, xvar, S_inv, n):
    t2 = n * np.dot(np.dot((x - xvar).T, S_inv), (x - xvar))
    return t2

def contar_puntos_sintetico(t2, lcs, l):
    arl = [0]
    crl = [0]
    for i in range(len(t2)):
        if t2[i] > lcs:
            arl.append(i)
            if i - arl[-2] < l:
                crl.append(i)
    return crl, arl

def calculate_arl(m, n, p, Delta, L, alpha=None, LCynt=None, return_values=False):
    # Generar la media y la matriz de covarianza
    mean = np.zeros(p)
    mean[-1] = Delta
    cov1 = np.eye(p)
    invcov = np.linalg.inv(cov1)

    # Generar datos multivariados normales
    data = np.random.multivariate_normal(mean, cov1, (m, n))
    meansv = np.mean(data, axis=1)

    # Calcular t2_values
    t2_values = np.array([carta_control_t2(x, np.zeros(p), invcov, n) for x in meansv])

    # Calcular el Límite de Control Superior (LCynt)
    if LCynt is not None:
        # Si se proporciona LCynt, se utiliza directamente
        LCynt_value = LCynt
    elif alpha is not None:
        # Si se proporciona alpha, se calcula LCynt
        LCynt_value = ((n - 1) * p / (n - p)) * f.ppf(1 - alpha, p, n - p)
    else:
        # Si no se proporciona ni LCynt ni alpha, se utiliza un valor por defecto
        alpha_default = 0.05
        LCynt_value = ((n - 1) * p / (n - p)) * f.ppf(1 - alpha_default, p, n - p)

    # Calcular CRL
    crl_points, arl_points = contar_puntos_sintetico(t2_values, LCynt_value, L)
    
    arl_points = np.diff(arl_points)

    # Calcular ARL Intercalado
    if len(crl_points) > 2:
        arl_intercalado = [crl_points[i + 2] - crl_points[i] for i in range(len(crl_points) - 2)]
        arl_intercalado_mean = np.mean(arl_intercalado) * 1.4
    else:
        arl_intercalado_mean = np.nan

    # Calcular ARL normal
    if len(crl_points) > 1:
        arl = np.mean(np.diff(crl_points))
    else:
        arl = np.nan

    crl_points = np.diff(crl_points)
    results = {
        'ARL': arl,
        'ARL_Intercalado': arl_intercalado_mean
    }

    # Retornar resultados y valores adicionales si return_values es True
    if return_values:
        return results, t2_values, arl_points, LCynt_value
    else:
        return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Inicializar variables para pasar a la plantilla
        m = n = p = Delta = L = alpha = LCynt = use_alpha = None

        try:
            # Validación de m, n, p, Delta, y L
            m = int(request.form['m'])
            n = int(request.form['n'])
            p = int(request.form['p'])
            Delta = float(request.form['Delta'])
            L = int(request.form['L'])

            # Validación de que los valores sean positivos
            if m <= 0 or n <= 0 or p <= 0 or L <= 0:
                raise ValueError("Los valores de m, n, p y L deben ser positivos.")

            # Verificar si el usuario eligió usar alpha o LCynt
            use_alpha = request.form.get('use_alpha')
            if use_alpha == 'alpha':
                alpha = float(request.form['alpha'])
                if not (0 < alpha < 1):
                    raise ValueError("Alpha debe estar entre 0 y 1.")
                LCynt = None
            elif use_alpha == 'LCynt':
                LCynt = float(request.form['LCynt'])
                if LCynt <= 0:
                    raise ValueError("LCynt debe ser un valor positivo.")
                alpha = None
            else:
                return render_template('index.html', error="Por favor seleccione si desea usar Alpha o LCynt.",
                                       m=m, n=n, p=p, Delta=Delta, L=L, alpha=alpha, LCynt=LCynt, use_alpha=use_alpha)

        except ValueError as e:
            return render_template('index.html', error=str(e),
                                   m=m, n=n, p=p, Delta=Delta, L=L, alpha=alpha, LCynt=LCynt, use_alpha=use_alpha)

        
        # Llamar a la función para calcular ARL y obtener t2_values y crl_points
        results, t2_values, crl_points, LCynt_value = calculate_arl(m, n, p, Delta, L, alpha=alpha, LCynt=LCynt, return_values=True)
        
        # Generar las gráficas y obtener el HTML
        grafica_t2 = graficar_t2_con_limite(t2_values, LCynt_value)
        grafica_arl = graficar_arl(crl_points, L)
        
        return render_template('index.html', results=results,
                               m=m, n=n, p=p, Delta=Delta, L=L, alpha=alpha, LCynt=LCynt, use_alpha=use_alpha,
                               grafica_t2=grafica_t2, grafica_arl=grafica_arl)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)