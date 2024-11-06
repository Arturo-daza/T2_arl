import plotly.graph_objects as go
import numpy as np 

def graficar_t2_con_limite(t2_values, LCynt, title='Gráfico de Control T² de Hotelling'):
    fig = go.Figure()

    # Añadir los valores de T² a la gráfica
    fig.add_trace(go.Scatter(
        x=np.arange(1, len(t2_values) + 1),
        y=t2_values,
        mode='lines+markers',
        name='Valores de T²'
    ))

    # Añadir el Límite de Control Superior a la gráfica
    fig.add_trace(go.Scatter(
        x=[1, len(t2_values)],
        y=[LCynt, LCynt],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Límite LCynt'
    ))

    # Configurar el diseño de la gráfica e incluir el rango deslizante en el eje x
    fig.update_layout(
        title=title,
        xaxis_title='Número de Muestra',
        yaxis_title='Valor de T²',
        template='plotly_white',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='linear'
        )
    )

    # Retornar el HTML de la gráfica
    return fig.to_html(full_html=False)

def graficar_arl(crl_points, L, title='Gráfico de CRL con Límite L'):
    import numpy as np
    import plotly.graph_objects as go

    fig = go.Figure()

    # Generar los índices para el eje x
    x_indices = np.arange(1, len(crl_points) + 1)

    # Crear una lista de colores basada en si el valor de CRL excede L
    colors = ['#FF073A' if crl > L else 'cyan' for crl in crl_points]

    # Añadir la línea que conecta los puntos de CRL
    fig.add_trace(go.Scattergl(
        x=x_indices,
        y=crl_points,
        mode='lines',
        line=dict(color='cyan', width=1),
        name='Línea de CRL',
        showlegend=False
    ))

    # Añadir los puntos de CRL con colores según la condición
    fig.add_trace(go.Scattergl(
        x=x_indices,
        y=crl_points,
        mode='markers',
        marker=dict(
            color=colors,
            size=6
        ),
        name='Valores de CRL'
    ))

    # Añadir el Límite L
    fig.add_trace(go.Scatter(
        x=[1, len(crl_points)],
        y=[L, L],
        mode='lines',
        line=dict(color='red', dash='dash', width=2),
        name=f'Límite L = {L}'
    ))

    # Configurar el rango del eje x
    x_min = 1
    x_max = len(crl_points)

    # Configurar el diseño de la gráfica
    fig.update_layout(
        title=title,
        xaxis_title='Índice del CRL',
        yaxis_title='Valor del CRL',
        template='plotly_dark',
        xaxis=dict(
            range=[x_min, x_max],
            rangeslider=dict(
                visible=True,
                range=[x_min, x_max]
            ),
            type='linear'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    # Retornar el HTML de la gráfica
    return fig.to_html(full_html=False)
