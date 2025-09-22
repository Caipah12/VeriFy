import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const MainInterface = () => {
  const [selectedArticle, setSelectedArticle] = useState(null);

  // Modal component for full article view
  const ArticleModal = ({ article, onClose }) => {
    if (!article) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg w-full max-w-4xl mx-4 p-6">
          <div className="flex justify-between items-center mb-4">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              article.label === 'True' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {article.label}
            </span>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
              <span className="text-2xl">×</span>
            </button>
          </div>
          <div className="prose max-w-none">
            <div className="text-gray-700 mt-4 leading-relaxed">
              {article.text}
            </div>
          </div>
          <div className="mt-6 flex justify-between items-center">
            <span className="text-sm text-purple-600">
              Similarity Score: {article.similarity_score}%
            </span>
            <button 
              onClick={onClose}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  // Similar Articles Panel
  const SimilarArticlesPanel = ({ similarArticles }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    if (!similarArticles || similarArticles.length === 0) return null;

    return (
      <Card className="mt-6">
        <CardHeader className="cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-semibold text-purple-900">
              Similar Articles Found
              <span className="ml-2 bg-purple-100 text-purple-800 text-sm px-2 py-1 rounded-full">
                {similarArticles.length}
              </span>
            </CardTitle>
            <span className="text-purple-600">
              {isExpanded ? '▼' : '▲'}
            </span>
          </div>
        </CardHeader>

        {isExpanded && (
          <CardContent className="divide-y divide-gray-100">
            {similarArticles.map((article, index) => (
              <div 
                key={index} 
                className="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={() => setSelectedArticle(article)}
              >
                <div className="flex justify-between items-start mb-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    article.label === 'True' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {article.label}
                  </span>
                  <span className="text-sm font-medium text-purple-600">
                    Similarity: {article.similarity_score}%
                  </span>
                </div>
                <div className="text-gray-700 text-sm mt-2 line-clamp-3">
                  {article.text}
                </div>
                <button 
                  className="mt-2 text-purple-600 text-sm hover:text-purple-800"
                  onClick={() => setSelectedArticle(article)}
                >
                  Read More →
                </button>
              </div>
            ))}
          </CardContent>
        )}
      </Card>
    );
  };

  return (
    <div className="w-full">
      <SimilarArticlesPanel similarArticles={similarArticles} />
      {selectedArticle && (
        <ArticleModal 
          article={selectedArticle} 
          onClose={() => setSelectedArticle(null)} 
        />
      )}
    </div>
  );
};

() => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left Column - News Analysis Section */}
        <div className="lg:w-8/12 space-y-8 flex-shrink-0">
          <div className="glass-card p-6 mb-8">
            {/* News Analysis Form */}
          </div>
          
          {/* Analysis Result Section */}
          {/* Charts and Stats Grid */}
        </div>

        {/* Right Column - Fixed Position Tips */}
        <div className="lg:w-4/12 flex-shrink-0">
          <div className="sticky top-24 space-y-6 max-h-[calc(100vh-6rem)] overflow-y-auto pb-6">
            {/* Daily Reminder */}
            <div className="glass-card p-6">
              {/* Daily Reminder Content */}
            </div>

            {/* iNaQ Section */}
            <div className="glass-card p-6">
              {/* iNaQ Content */}
            </div>

            {/* Quick Tips */}
            <div className="glass-card p-6">
              {/* Quick Tips Content */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainInterface;