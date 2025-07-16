"use client";

import { useState } from "react";

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
        throw new Error(`Erro da API: ${res.status}`);
      }

      const data = await res.json();

      // Supondo que sua API retorna { summary: "texto do resumo" } ou similar
      setSummary(data.summary || JSON.stringify(data));
    } catch (err: any) {
      setError(err.message || "Erro desconhecido");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h1>Resumidor de Artigos</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <input
          type="url"
          placeholder="Cole o link da Wikipedia aqui"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
        />
        <button type="submit" disabled={loading} style={{ marginTop: "0.5rem", padding: "0.5rem 1rem" }}>
          {loading ? "Carregando..." : "Gerar Resumo"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>Erro: {error}</p>}

      {summary && (
        <section style={{ whiteSpace: "pre-wrap", padding: "1rem", borderRadius: "4px" }}>
          <h2>Resumo:</h2>
          <p>{summary}</p>
        </section>
      )}
    </main>
  );
}
