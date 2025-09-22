import React from 'react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const SimilarityDisplay = ({ prediction, confidenceScore, similarArticles }) => {
  return (
    <div className="space-y-4">
      {/* Main Prediction Alert */}
      <Alert className={`${prediction === 'True' ? 'bg-green-50' : 'bg-red-50'}`}>
        <AlertTitle className={`text-lg font-semibold ${prediction === 'True' ? 'text-green-800' : 'text-red-800'}`}>
          {prediction === 'True' ? 'This News Appears to be Legitimate' : 'This News May be Fake'}
        </AlertTitle>
        <AlertDescription>
          AI Confidence Score: {confidenceScore.toFixed(1)}%
        </AlertDescription>
      </Alert>

      {/* Similar Articles Section */}
      {similarArticles && similarArticles.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Similar Articles Found
          </h3>
          <div className="space-y-4">
            {similarArticles.map((article, index) => (
              <div key={index} className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-sm font-medium text-purple-600">
                    Similarity Score: {article.similarity_score}%
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    article.label === 'True' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {article.label}
                  </span>
                </div>
                <p className="text-gray-600 text-sm">{article.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SimilarityDisplay;