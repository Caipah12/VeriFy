import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function AdminDashboard() {
  const [dashboardData, setDashboardData] = useState({
    userSubmissions: 0,
    totalArticles: 0,
    flaggedAsFake: 0,
    lastTrained: 'N/A',
    modelStatus: 'N/A'
  });
  const [fakeArticles, setFakeArticles] = useState([]);

  useEffect(() => {
    // Get the data from the window object where Flask template rendered it
    const data = window.dashboardData;
    if (data) {
      setDashboardData({
        userSubmissions: data.user_submissions,
        totalArticles: data.total_articles,
        flaggedAsFake: data.flagged_as_fake,
        lastTrained: data.last_trained,
        modelStatus: data.model_status
      });
      setFakeArticles(data.fake_articles);
    }
  }, []);

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-purple-900">Dashboard</h2>
        <div className="flex items-center gap-2">
          <span>Welcome back</span>
          <span className="font-bold">Admin User</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User Submissions Card */}
        <Card className="bg-purple-500 text-white">
          <CardHeader>
            <CardTitle>User Submissions</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{dashboardData.userSubmissions}</p>
          </CardContent>
        </Card>

        {/* Total Articles Card */}
        <Card className="bg-orange-500 text-white">
          <CardHeader>
            <CardTitle>Total Articles</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{dashboardData.totalArticles}</p>
          </CardContent>
        </Card>

        {/* Flagged as Fake Card with Dialog */}
        <Dialog>
          <DialogTrigger asChild>
            <Card className="bg-red-500 text-white cursor-pointer hover:bg-red-600 transition-colors">
              <CardHeader>
                <CardTitle>Flagged as Fake</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-4xl font-bold">{dashboardData.flaggedAsFake}</p>
              </CardContent>
            </Card>
          </DialogTrigger>
          <DialogContent className="max-w-4xl">
            <DialogHeader>
              <DialogTitle>Fake News Articles</DialogTitle>
            </DialogHeader>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="px-4 py-2 text-left border-b">ID</th>
                    <th className="px-4 py-2 text-left border-b">Content</th>
                    <th className="px-4 py-2 text-left border-b">Created At</th>
                  </tr>
                </thead>
                <tbody>
                  {fakeArticles.map((article) => (
                    <tr key={article.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 border-b">{article.id}</td>
                      <td className="px-4 py-2 border-b max-w-xl truncate">
                        {article.content}
                      </td>
                      <td className="px-4 py-2 border-b">{article.created_at}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Model Status Card */}
      <Card className="bg-green-500 text-white mt-6">
        <CardHeader>
          <CardTitle>Model Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <p>Last Trained: {dashboardData.lastTrained}</p>
            <p>Status: {dashboardData.modelStatus}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}