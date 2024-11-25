import plotly.graph_objects as go
import numpy as np 

class GraphGenerator:
    @staticmethod
    def graficar_t2_con_limite(t2_values, LCynt, title='Subgráfico de Control T² de Hotelling'):
        """
        Generates an interactive plotly graph for Hotelling's T² control chart with a specified control limit.
        Parameters:
        t2_values (list or array-like): A sequence of T² values to be plotted.
        LCynt (float): The upper control limit for the T² values.
        title (str, optional): The title of the graph. Default is 'Subgráfico de Control T² de Hotelling'.
        Returns:
        str: The HTML representation of the plotly graph.
        """
        
        # Antes de graficar T²
        # t2_values = GraphGenerator.downsample_data(t2_values, max_points=1000)
        t2_values = t2_values[:1000]


        
        fig = go.Figure()

        x_values = np.arange(1, len(t2_values) + 1)

        # Crear una lista de colores basada en si el valor de T² excede LCynt
        colors = ['#FF073A' if t > LCynt else '#39FF14' for t in t2_values]  # Rojo neón y verde neón

        # Añadir la línea que conecta los puntos (solo para los puntos dentro del límite)
        fig.add_trace(go.Scattergl(
            x=x_values,
            y=t2_values,
            mode='lines',
            line=dict(color='#39FF14', width=1),
            name='Línea de T²',
            showlegend=False
        ))

        # Añadir los puntos de T² con colores según la condición
        fig.add_trace(go.Scattergl(
            x=x_values,
            y=t2_values,
            mode='markers',
            marker=dict(
                color=colors,
                size=6
            ),
            name='Valores de T²'
        ))

        # Añadir el Límite de Control Superior
        fig.add_trace(go.Scatter(
            x=[1, len(t2_values)],
            y=[LCynt, LCynt],
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            name=f'Límite LCynt = {LCynt}'
        ))

        # Configurar el rango del eje x
        x_min = 1
        x_max = len(t2_values)

        # Configurar el diseño de la gráfica e incluir el rango deslizante en el eje x
        fig.update_layout(
            title=title,
            xaxis_title='Número de Muestra',
            yaxis_title='Valor de T²',
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
    
    @staticmethod
    def graficar_crl(crl_points, L, title='Subgráfico de CRL con Límite L'):
        """
        Generates an interactive plot of CRL points with a specified limit L using Plotly.
        Parameters:
        crl_points (list or array-like): A list or array of CRL (conforming run length) values to be plotted.
        L (float): The limit value to be plotted as a dashed red line.
        title (str, optional): The title of the plot. Default is 'Subgráfico de CRL con Límite L'.
        Returns:
        str: The HTML representation of the plot.
        """
        
        # Antes de graficar CRL
        # crl_points = GraphGenerator.downsample_data(crl_points, max_points=1000)
        crl_points = crl_points[:1000]
        

        fig = go.Figure()

        # Generar los índices para el eje x
        x_indices = np.arange(1, len(crl_points) + 1)

        # Crear una lista de colores basada en si el valor de CRL excede L
        colors = ['#FF073A' if crl < L else 'cyan' for crl in crl_points]

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
    
    
    
    def downsample_data(data, max_points=1000):
        """
        Reduce the number of points in the data to a maximum of max_points.
        Parameters:
        data (list or array-like): Original data to be downsampled.
        max_points (int): Maximum number of points to retain.
        Returns:
        list: Downsampled data.
        """
        if len(data) > max_points:
            indices = np.linspace(0, len(data) - 1, max_points, dtype=int)
            return data[indices]
        return data


