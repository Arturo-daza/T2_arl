from flask import Flask, render_template, request
from arl_calculator import ARLCalculator
from graph_generator import GraphGenerator

app = Flask(__name__)
arl_calculator = ARLCalculator()
graph_generator = GraphGenerator()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            m = int(request.form['m'])
            n = int(request.form['n'])
            p = int(request.form['p'])
            Delta = float(request.form['Delta'])
            L = int(request.form['L'])
            use_alpha = request.form.get('use_alpha')

            alpha, LCynt = None, None
            if use_alpha == 'alpha':
                alpha = float(request.form['alpha'])
            elif use_alpha == 'LCynt':
                LCynt = float(request.form['LCynt'])

            results, t2_values, crl_points, LCynt_value = arl_calculator.calculate_arl(
                m, n, p, Delta, L, alpha=alpha, LCynt=LCynt
            )

            grafica_t2 = graph_generator.graficar_t2_con_limite(t2_values, LCynt_value)
            grafica_crl = graph_generator.graficar_arl(crl_points, L)

            return render_template('index.html', results=results,
                               m=m, n=n, p=p, Delta=Delta, L=L, alpha=alpha, LCynt=LCynt, use_alpha=use_alpha,
                               grafica_t2=grafica_t2, grafica_crl=grafica_crl)

        except ValueError as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
