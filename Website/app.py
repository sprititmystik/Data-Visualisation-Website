import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for
import pandas as pd
import os

# Load the data from the CSV file
file_path = 'Finance_data.csv'
data = pd.read_csv(file_path)

# Define the columns for x and y axis options
x_axis_options = ['gender', 'Investment_Avenues', 'Duration', 'Avenue', 'age']
y_axis_options = ['Mutual_Funds', 'Equity_Market', 'Debentures', 'Government_Bonds', 'Fixed_Deposits', 'Gold']

app = Flask(__name__)

@app.route('/')
def home():
    top_data = data.head()
    top_data_html = top_data.to_html(classes='table table-sm table-bordered', index=False)
    return render_template('home.html', table=top_data_html)

@app.route('/create-graph', methods=['GET', 'POST'])
def create_graph():
    plot_url = None
    if request.method == 'POST':
        graph_type = request.form.get('graph_type')
        x_axis = request.form.get('x_axis')
        y_axis = request.form.get('y_axis')

        # Generate the graph based on user input
        fig, ax = plt.subplots(figsize=(8, 5))

        if graph_type == 'bar':
            data.groupby(x_axis)[y_axis].mean().plot(kind='bar', ax=ax, color='blue')
        elif graph_type == 'line':
            data.plot(kind='line', x=x_axis, y=y_axis, ax=ax, color='green')
        elif graph_type == 'scatter':
            data.plot(kind='scatter', x=x_axis, y=y_axis, ax=ax, color='red')

        plt.title(f'{graph_type.capitalize()} Graph of {y_axis} vs {x_axis}')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.tight_layout()

        plot_path = os.path.join('static', 'user_plot.png')
        plt.savefig(plot_path)
        plt.close()

        plot_url = url_for('static', filename='user_plot.png')

    return render_template('create_graph.html', x_options=x_axis_options, y_options=y_axis_options, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
