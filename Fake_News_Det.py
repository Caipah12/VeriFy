from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the model and vectorizer with error handling
try:
    with open(r'C:\best_news_model.pkl', 'rb') as f:
        data = pickle.load(f)
        loaded_model = data[0]
        tfvect = data[1]
except Exception as e:
    print(f"Error loading model/vectorizer: {e}")

# Load dataset with error handling
try:
    dataframe = pd.read_csv(
        'C:/news.csv',
        encoding='ISO-8859-1'
    )
    x = dataframe['text']
    tfid_x_train = tfvect.transform(x)
except Exception as e:
    print(f"Error loading dataset: {e}")

def fake_news_det(news):
    """Predict whether the news is fake or true."""
    try:
        input_data = [news]
        vectorized_input = tfvect.transform(input_data)

        # Calculate cosine similarity for debugging purposes
        similarities = cosine_similarity(vectorized_input, tfid_x_train)
        max_similarity = similarities.max()
        print(f"Max Similarity Score: {max_similarity}")

        # Predict using the loaded model
        prediction = loaded_model.predict(vectorized_input)
        print(f"Prediction: {prediction[0]}")
        
        # Return binary prediction
        return 'True' if prediction[0] == 1 else 'Fake'
    except Exception as e:
        print(f"Prediction Error: {e}")
        return "Error: Unable to predict"

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', prediction=None, error=None)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        message = request.form.get('message', '')
        print(f"Received Message: {message}")
        pred = fake_news_det(message)
        return render_template('index.html', prediction=pred, error=None)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return render_template('index.html', prediction=None, error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
