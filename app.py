from flask import Flask, render_template, send_file, request, jsonify
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = Flask(__name__)

# Time Data
#np.random.seed(0)
#dates = pd.date_range(start='2022-01-01', periods=100, freq='ME')

# Generar datos de ejemplo
np.random.seed(0)
date_range = pd.date_range(start='2023-01-01', periods=5, freq='ME')
data = pd.DataFrame({
    'Date': date_range,
    'Value': np.random.randn(5).cumsum()
})


@app.route('/')
def index():
    
    # Datos del KPI
    kpi_values = {
        'kpi6': 140495,
        'kpi7': 140495,
        'kpi8': 140495,
        'kpi9': 140495,
        'kpi10': 140495,
        'kpi11': 140495
    }
    
    #graph_htmls = {
    #    'graph1': MRR_HTML,
    #    'graph2': CHARGEABLE_HTML,
    #    'graph3': CUSTOMERS_HTML,
    #    'graph4': ARPU_HTML,
    #    'graph5': CHURN_HTML
    #}
    
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')

    return render_template('index.html', 
                           kpi_value=kpi_values,
                           start_date=start_date.strftime('%Y-%m-%d'),
                           end_date=end_date.strftime('%Y-%m-%d'),
                           month_range=f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    #return render_template('index.html', graph_html=graph_htmls, kpi_value=kpi_values)


@app.route('/api/graph_data1')
def graph_data1():
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
    
    ################################################################### MRR LINE PLOT
    # Create Figure
    fig = go.Figure()

    # Add Data and Colors to Plot
    fig.add_trace(go.Scatter(
        # Data
        x=filtered_data['Date'].tolist(), 
        y=filtered_data['Value'].tolist(), 
        mode='lines+markers', 
        name='Serie Temporal',

        # Line and Fill Color
        line=dict(color='#FFFFFF', width=1),
        fill='tozeroy',  # Llena el área debajo de la línea
        fillcolor='rgba(0, 242, 222, 1)'  # Color de llenado con transparencia
    ))

    # Setup Figure
    fig.update_layout(#xaxis_title='Fecha',
                      #yaxis_title='Valor',
                      plot_bgcolor='rgba(0,0,0,0)',  # Fondo del gráfico transparente
                      paper_bgcolor='rgba(0,0,0,0)',  # Fondo del área de papel transparente
                      xaxis_rangeslider_visible=False,
                      xaxis_tickformat='%d-%b-%y',
                      xaxis=dict(
                          showgrid=False,  # Sin líneas de cuadrícula en el eje x
                          tickangle=15,  # Rotar los ticks del eje x para mejor legibilidad
                          tickmode='array',  # Usar modo array para definir los ticks
                          ticktext=[date_range[i].strftime('%m-%y') for i in range(0, len(date_range), 8)]  # Mostrar fechas en formato día-mes
                      ),
                      yaxis=dict(showgrid=False),  # Sin líneas de cuadrícula en el eje y
                      font=dict(color='white'),  # Color del texto en el gráfico
                      width=560,  # Ancho de la gráfica en píxeles
                      height=320  # Alto de la gráfica en píxeles
                      
                      )  # Mostrar solo fecha sin hora

    graph_data = fig.to_plotly_json()
    
    return jsonify(graph_data)

@app.route('/api/graph_data2')
def graph_data2():
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
    
    ################################################################### CHARGEABLE SIM'S LINE PLOT
    # Create Figure
    fig = go.Figure()
    
    # Add Data and Colors to Plot
    fig.add_trace(go.Scatter(
        # Data
        x=filtered_data['Date'].tolist(), 
        y=filtered_data['Value'].tolist(), 
        mode='lines+markers', 
        name='Serie Temporal',
    
        # Line and Fill Color
        line=dict(color='#FFFFFF', width=1),
        fill='tozeroy',  # Llena el área debajo de la línea
        fillcolor='rgba(83, 18, 212, 1)'  # Color de llenado con transparencia
    ))
    
    # Setup Figure
    fig.update_layout(
        #xaxis_title='Fecha',
        #yaxis_title='Valor',
        plot_bgcolor='rgba(0,0,0,0)',   # Fondo del gráfico transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del área de papel transparente
        xaxis_rangeslider_visible=False,
        xaxis_tickformat='%d-%b-%y',
        #xaxis_title_font=dict(size=12, color='white', family='Segoe UI', weight='bold'),  # Tamaño y color del título del eje x
        #yaxis_title_font=dict(size=12, color='white', family='Segoe UI', weight='bold'),  # Tamaño y color del título del eje y
        xaxis=dict(
            showgrid=False,  # Sin líneas de cuadrícula en el eje x
            tickangle=15,  # Rotar los ticks del eje x para mejor legibilidad
            tickmode='array',  # Usar modo array para definir los ticks
            ticktext=[date_range[i].strftime('%m-%y') for i in range(0, len(date_range), 8)]  # Mostrar fechas en formato día-mes
        ),
        yaxis=dict(showgrid=False),  # Sin líneas de cuadrícula en el eje y
        font=dict(color='white'),  # Color del texto en el gráfico
        width=560,  # Ancho de la gráfica en píxeles
        height=320  # Alto de la gráfica en píxeles
    )


    graph_data = fig.to_plotly_json()
    
    return jsonify(graph_data)


@app.route('/api/graph_data3')
def graph_data3():
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')

    ################################################################### NEW ACTIVE CUSTOMERS BAR PLOT

    # Crear la figura de gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=filtered_data['Date'].tolist(), 
        y=filtered_data['Value'].tolist(), 
        marker_color='#02EF9D'  # Color personalizado para las barras
    )])
    
    # Configurar el diseño del gráfico
    fig.update_layout(
        #xaxis_title='Categorías',
        #yaxis_title='Valores',
        xaxis=dict(
            showgrid=False,  # Sin líneas de cuadrícula en el eje x
            tickangle=15,  # Rotar los ticks del eje x para mejor legibilidad
            tickmode='array',  # Usar modo array para definir los ticks
            ticktext=[date_range[i].strftime('%m-%y') for i in range(0, len(date_range), 8)]  # Mostrar fechas en formato día-mes
        ),
        yaxis=dict(
            #tickvals=[],  # Elimina los valores del eje Y
            showticklabels=True,  # También oculta las etiquetas de los ticks
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo del área del gráfico transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del lienzo del gráfico transparente
        xaxis_rangeslider_visible=False,
        xaxis_tickformat='%d-%b-%y',
        font=dict(color='white'),  # Color del texto en el gráfico
        width=465,  # Ancho de la gráfica en píxeles
        height=265  # Alto de la gráfica en píxeles
    )

    graph_data = fig.to_plotly_json()
    
    return jsonify(graph_data)


@app.route('/api/graph_data4')
def graph_data4():
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
    
    ################################################################### ARPU LINE PLOT
    # Create Figure
    fig = go.Figure()
    
    # Add Data and Colors to Plot
    fig.add_trace(go.Scatter(
        # Data
        x=filtered_data['Date'].tolist(), 
        y=filtered_data['Value'].tolist(), 
        mode='lines+markers', 
        name='Serie Temporal',
    
        # Line and Fill Color
        line=dict(color='#FFFFFF', width=1),
        fill='tozeroy',  # Llena el área debajo de la línea
        fillcolor='rgba(49, 111, 188, 1)'  # Color de llenado con transparencia
    ))
    
    # Setup Figure
    fig.update_layout(
        #xaxis_title='Fecha',
        #yaxis_title='Valor',
        #xaxis_title_font=dict(size=12, color='white', family='Segoe UI', weight='bold'),  # Tamaño y color del título del eje x
        #yaxis_title_font=dict(size=12, color='white', family='Segoe UI', weight='bold'),  # Tamaño y color del título del eje y
        xaxis=dict(
            showgrid=False,  # Sin líneas de cuadrícula en el eje x
            tickangle=15,  # Rotar los ticks del eje x para mejor legibilidad
            tickmode='array',  # Usar modo array para definir los ticks
            ticktext=[date_range[i].strftime('%m-%y') for i in range(0, len(date_range), 8)]  # Mostrar fechas en formato día-mes
        ),
        yaxis=dict(
            #tickvals=[],  # Elimina los valores del eje Y
            showticklabels=True,  # También oculta las etiquetas de los ticks
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo del área del gráfico transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del lienzo del gráfico transparente
        xaxis_rangeslider_visible=False,
        xaxis_tickformat='%d-%b-%y',
        font=dict(color='white'),  # Color del texto en el gráfico
        width=465,  # Ancho de la gráfica en píxeles
        height=265  # Alto de la gráfica en píxeles
    )
    
    graph_data = fig.to_plotly_json()
    
    return jsonify(graph_data)


@app.route('/api/graph_data5')
def graph_data5():
    month_range_input = request.args.get('month_range', default='')

    start_date = end_date = None
    
    if 'to' in month_range_input:
        parts = month_range_input.split(' to ')
        if len(parts) == 2:
            start_date, end_date = parts
    else:
        start_date = date_range[0].strftime('%Y-%m-%d')
        end_date = date_range[-1].strftime('%Y-%m-%d')
    
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        start_date = date_range[0]
        end_date = date_range[-1]

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')

    ################################################################### CHURN SIM's BAR PLOT

    # Crear la figura de gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=filtered_data['Date'].tolist(), 
        y=filtered_data['Value'].tolist(), 
        marker_color='#5312D4'  # Color personalizado para las barras
    )])
    
    # Configurar el diseño del gráfico
    fig.update_layout(
        #xaxis_title='Categorías',
        #yaxis_title='Valores',
        xaxis=dict(
            showgrid=False,  # Sin líneas de cuadrícula en el eje x
            tickangle=15,  # Rotar los ticks del eje x para mejor legibilidad
            tickmode='array',  # Usar modo array para definir los ticks
            ticktext=[date_range[i].strftime('%m-%y') for i in range(0, len(date_range), 8)]  # Mostrar fechas en formato día-mes
        ),
        yaxis=dict(
            #tickvals=[],  # Elimina los valores del eje Y
            showticklabels=True,  # También oculta las etiquetas de los ticks
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Fondo del área del gráfico transparente
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo del lienzo del gráfico transparente
        xaxis_rangeslider_visible=False,
        xaxis_tickformat='%d-%b-%y',
        font=dict(color='white'),  # Color del texto en el gráfico
        width=465,  # Ancho de la gráfica en píxeles
        height=265  # Alto de la gráfica en píxeles
    )

    
    graph_data = fig.to_plotly_json()
    
    return jsonify(graph_data)


if __name__ == '__main__':
    app.run(debug=True)
