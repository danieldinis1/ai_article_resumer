"use client";

import { useState } from "react";


//run -> npm run dev             
export default function Page() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setSummary(null);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/resume", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!res.ok) {
        throw new Error(`Please provide a valid Wikipedia URL. Status: ${res.status}`);
      }

      const data = await res.json();

      setSummary(data.summary || JSON.stringify(data));
    } catch (err: any) {
      setError(err.message || "Erro desconhecido");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <main className="w-full max-w-md p-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-6">Article Resumer</h1>

        <form onSubmit={handleSubmit} className="w-full">
          <input
            type="url"
            placeholder="Paste your wikipedia URL here"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            className="w-full p-2 border border-gray-300 rounded-md mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Loading..." : "Generate Resume"}
          </button>
        </form>

        {error && (
          <p className="text-red-500 text-center mt-4">Error: {error}</p>
        )}

        {summary && (
          <section className="mt-6 p-4 bg-gray-100 dark:bg-gray-700 rounded-md">
            <h2 className="text-xl font-semibold mb-2">Resume:</h2>
            <p className="whitespace-pre-wrap text-gray-800 dark:text-gray-200">{summary}</p>
          </section>
        )}
      </main>
    </div>
  );
}