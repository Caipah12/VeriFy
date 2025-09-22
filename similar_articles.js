import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const SimilarArticles = ({ articles = [] }) => {
  const [expandedArticle, setExpandedArticle] = useState(null);

  const createPreview = (text) => {
    const words = text.split(' ').slice(0, 50).join(' ');
    return words + (text.split(' ').length > 50 ? '...' : '');
  };

  if (articles.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-bold text-purple-800 mb-4">Similar Articles Found</h3>
      <div className="space-y-4">
        {articles.map((article, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
            <div className="flex justify-between items-start mb-4">
              <span className="text-sm font-medium text-purple-600">
                Similarity Score: {article.similarity_score}%
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                article.label === 'True' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {article.label}
              </span>
            </div>

            <div className="prose max-w-none">
              <p className="text-gray-700">
                {expandedArticle === index ? article.text : createPreview(article.text)}
              </p>
            </div>

            <button
              onClick={() => setExpandedArticle(expandedArticle === index ? null : index)}
              className="mt-4 flex items-center text-purple-600 hover:text-purple-800 transition-colors duration-200"
            >
              {expandedArticle === index ? (
                <>
                  <span className="mr-2">Read Less</span>
                  <ChevronUp className="w-4 h-4" />
                </>
              ) : (
                <>
                  <span className="mr-2">Read More</span>
                  <ChevronDown className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SimilarArticles;