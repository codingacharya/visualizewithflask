from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# Load dataset (modify path as needed)
df = pd.read_csv('data.csv')  # Replace 'data.csv' with your dataset

@app.route('/', methods=['GET', 'POST'])
def index():
    img = None
    columns = df.columns.tolist()
    
    if request.method == 'POST':
        x_col = request.form.get('x_column')
        y_col = request.form.get('y_column')
        
        if x_col and y_col:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=df[x_col], y=df[y_col])
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f'Scatter Plot of {x_col} vs {y_col}')
            
            # Save plot to a string buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
    
    return render_template('index.html', columns=columns, img=img)

if __name__ == '__main__':
    app.run(debug=True)
