import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import traceback
import time
import re 

class NewsModel:
    def __init__(self, model_path, dataset_path):
        self.loaded_model = None
        self.tfvect = None
        self.tfid_x_train = None 
        self.dataset = None
        self.evaluation_metrics = {
            'confidence_scores': [],
            'predictions': [],
            'true_labels': [],
            'processing_times': [],
            'dataset_sizes': []
        }
        self.load_model(model_path)
        self.load_dataset(dataset_path)

    def clean_text(self, text):
        """Clean text using the same preprocessing steps as training data"""
        try:
            if not isinstance(text, str):
                raise ValueError("Input must be a string")
                
            text = text.strip()
            if not text:
                raise ValueError("Input cannot be empty")
                
            if len(text) < 10:
                raise ValueError("Text is too short. Minimum length is 10 characters.")
                
            # Basic text cleaning
            text = ' '.join(text.split())
            text = re.sub(r'[^\w\s.,!?-]', '', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'([.,!?])\1+', r'\1', text)
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            text = re.sub(r'\S+@\S+', '', text)
            
            text = text.strip()
            if not text:
                raise ValueError("Text became empty after cleaning")
                
            return text
            
        except Exception as e:
            raise ValueError(f"Text cleaning failed: {str(e)}")
        
    def load_model(self, model_path):
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.loaded_model, self.tfvect = data
        except Exception as e:
            print(f"Error loading model: {e}")

    def load_dataset(self, dataset_path):
        try:
            self.dataset = pd.read_csv(dataset_path, encoding='ISO-8859-1')
            self.dataset['text'] = self.dataset['text'].fillna('')
            self.dataset['label'] = self.dataset['label'].fillna('Unknown')
            self.dataset = self.dataset[self.dataset['text'].str.len() > 0]
            self.dataset['text'] = self.dataset['text'].astype(str)
            self.tfid_x_train = self.tfvect.transform(self.dataset['text'])
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def get_decision_score(self, vectorized_input):
        try:
            if hasattr(self.loaded_model, 'predict_proba'):
                proba = self.loaded_model.predict_proba(vectorized_input)[0]
                return abs(proba[1] - 0.5) * 2
            elif hasattr(self.loaded_model, 'decision_function'):
                return self.loaded_model.decision_function(vectorized_input)[0]
            else:
                predictions = [estimator.predict(vectorized_input)[0] 
                             for estimator in self.loaded_model.estimators_]
                agreement = sum(predictions) / len(predictions)
                return abs(agreement - 0.5) * 2
        except Exception as e:
            print(f"Error getting decision score: {e}")
            return 0.5

    def calculate_confidence_score(self, decision_score, similarity_score, prediction):
        try:
            abs_decision_score = abs(decision_score)
            normalized_decision = min(abs_decision_score, 1.0)
            
            base_confidence = 65 + (normalized_decision * 15)
            
            if similarity_score < 70:
                similarity_penalty = ((70 - similarity_score) / 70) * 20
                adjusted_confidence = max(65, base_confidence - similarity_penalty)
            else:
                similarity_boost = ((similarity_score - 70) / 30) * 10
                adjusted_confidence = min(95, base_confidence + similarity_boost)

            if prediction == 1:  # True news
                if similarity_score < 50:
                    adjusted_confidence = min(adjusted_confidence * 0.9, 75)
                elif similarity_score > 85 and normalized_decision > 0.8:
                    adjusted_confidence = min(adjusted_confidence * 1.1, 95)
            else:  # Fake news
                if similarity_score < 50:
                    adjusted_confidence = min(adjusted_confidence * 1.1, 90)
                elif similarity_score > 85:
                    adjusted_confidence = adjusted_confidence * 0.95

            variation = np.random.uniform(-1, 1)
            adjusted_confidence += variation
            
            final_confidence = round(min(95, max(65, adjusted_confidence)), 1)
            self.evaluation_metrics['confidence_scores'].append(final_confidence)
            return final_confidence
            
        except Exception as e:
            print(f"Error calculating confidence: {e}")
            return 65.0

    def find_similar_articles(self, vectorized_input):
        try:
            similarities = cosine_similarity(vectorized_input, self.tfid_x_train)
            similar_indices = similarities[0].argsort()[-3:][::-1]
            similar_articles = []

            for idx in similar_indices:
                similarity = similarities[0][idx]
                if similarity > 0.3:
                    article = {
                        'text': self.dataset.iloc[idx]['text'],
                        'similarity_score': round(similarity * 100, 2),
                        'label': self.dataset.iloc[idx]['label']
                    }
                    similar_articles.append(article)
                    
            print("Found similar articles:", similar_articles)  # Debug print
            return similar_articles
        except Exception as e:
            print(f"Error finding similar articles: {e}")
            return []

    def predict(self, news, true_label=None):
        """Predict whether news is fake or true, including text cleaning"""
        try:
            start_time = time.time()
            
            # Clean the input text first
            cleaned_news = self.clean_text(news)
            
            # Transform cleaned text
            input_data = [cleaned_news]
            vectorized_input = self.tfvect.transform(input_data)
            
            # Get model prediction
            prediction = self.loaded_model.predict(vectorized_input)[0]
            decision_score = self.get_decision_score(vectorized_input)
            
            # Calculate similarities
            similarities = cosine_similarity(vectorized_input, self.tfid_x_train)
            max_similarity = max(similarities[0]) * 100
            
            # Adjust prediction for low similarity scores
            if max_similarity < 70 and prediction == 1:
                prediction = 0
            
            # Convert prediction to label
            predicted_label = 'True' if prediction == 1 else 'Fake'
            
            # Update evaluation metrics
            self.evaluation_metrics['predictions'].append(predicted_label)
            if true_label is not None:
                self.evaluation_metrics['true_labels'].append(true_label)
            
            # Calculate confidence score
            confidence_score = self.calculate_confidence_score(
                decision_score,
                max_similarity,
                prediction
            )
            
            # Find similar articles
            similar_articles = self.find_similar_articles(vectorized_input)
            
            # Record processing time
            processing_time = time.time() - start_time
            self.evaluation_metrics['processing_times'].append(processing_time)
            
            return (predicted_label, confidence_score, similar_articles)
            
        except ValueError as e:
            print(f"Validation error: {e}")
            raise e
            
        except Exception as e:
            print(f"Prediction error: {e}")
            traceback.print_exc()
            return ("Error", 50.0, [])