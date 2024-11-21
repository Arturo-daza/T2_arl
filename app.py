from flask import Flask, render_template, request
from arl_calculator import ARLCalculator
from graph_generator import GraphGenerator

app = Flask(__name__)
arl_calculator = ARLCalculator()
graph_generator = GraphGenerator()

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the index route for the web application.
    If the request method is POST, it validates the input, performs calculations,
    generates graphs, and renders the 'index.html' template with the results and graphs.
    If there are validation errors or unexpected errors, it renders the 'index.html' 
    template with the appropriate error message.
    Returns:
        str: Rendered HTML template for the index page.
    """
    
    if request.method == 'POST':
        try:
            # Validar entrada
            m, n, p, Delta, L, alpha, LCynt = validate_input(request)
            
            print(m, n, p, Delta, L, alpha, LCynt)

            # Realizar cálculos
            results, t2_values, crl_points, LCynt_value = arl_calculator.calculate_arl(
                m, n, p, Delta, L, alpha=alpha, LCynt=LCynt
            )
            
            print(results, LCynt_value)

            # Generar gráficas
            grafica_t2 = graph_generator.graficar_t2_con_limite(t2_values, LCynt_value)
            grafica_crl = graph_generator.graficar_arl(crl_points, L)

            return render_template(
                'index.html',
                results=results,
                m=m, n=n, p=p, Delta=Delta, L=L, alpha=alpha, LCynt=LCynt,
                grafica_t2=grafica_t2, grafica_crl=grafica_crl
            )

        except ValueError as e:
            # Manejo específico de errores de validación
            return render_template('index.html', error=str(e))
        except Exception as e:
            # Manejo de errores inesperados
            return render_template('index.html', error="Error inesperado: " + str(e))

    return render_template('index.html')

def validate_input(request):
    """
    Validates and converts input values from a request form.
    Parameters:
    request (flask.Request): The request object containing form data.
    Returns:
    tuple: A tuple containing the validated and converted values:
        - m (int): An integer between 1000 and 1,000,000.
        - n (int): An integer between 2 and 25.
        - p (int): An integer between 1 and 15.
        - Delta (float): A float value.
        - L (int): An integer.
        - alpha (float or None): A float between 0 and 1 if 'use_alpha' is 'alpha', otherwise None.
        - LCynt (float or None): A positive float if 'use_alpha' is 'LCynt', otherwise None.
    Raises:
    ValueError: If any of the validation rules are not met or if required fields are missing.
    """

    try:
        # Validar y convertir valores
        m = int(request.form['m'])
        n = int(request.form['n'])
        p = int(request.form['p'])
        Delta = float(request.form['Delta'])
        L = int(request.form['L'])
        use_alpha = request.form.get('use_alpha')

        alpha, LCynt = None, None

        # Reglas de validación
        if not (1000 <= m <= 1000000):
            raise ValueError("El valor de m debe estar entre 1000 y 1,000,000.")
        if not (2 <= n <= 25):
            raise ValueError("El valor de n debe estar entre 2 y 25.")
        if not (1 <= p <= 15):
            raise ValueError("El valor de p debe estar entre 1 y 15.")
        if use_alpha == 'alpha':
            alpha = float(request.form['alpha'])
            if not (0 < alpha < 1):
                raise ValueError("Alpha debe estar entre 0 y 1.")
        elif use_alpha == 'LCynt':
            LCynt = float(request.form['LCynt'])
            if LCynt <= 0:
                raise ValueError("LCynt debe ser un valor positivo.")
        else:
            raise ValueError("Debe seleccionar una opción válida: Alpha o LCynt.")

        return m, n, p, Delta, L, alpha, LCynt

    except KeyError as e:
        raise ValueError(f"Falta el campo requerido: {str(e)}.")
    except ValueError as e:
        raise ValueError(f"Error en la conversión de datos: {str(e)}.")

if __name__ == '__main__':
    app.run(debug=True)
