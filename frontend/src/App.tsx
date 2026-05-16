import React, { useState } from 'react'
import './styles/global.css'
import ReactMarkdown from 'react-markdown'
import { FaSearch } from 'react-icons/fa'

function App() {
  const [search, setSearch] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [video, setVideo] = useState('')

  async function handleSearch() {
  if (!search) return

  setLoading(true)
  setResult('')

  try {
    const response = await fetch(
      `http://localhost:8000/career/${search}`
    )

    const data = await response.json()

    console.log(data)

    if (data.text) {
      setResult(data.text)
      setVideo(data.video)
    } else if (data.error) {
      setResult("Erro da IA: " + data.error)
    } else {
      setResult("Nenhuma resposta encontrada.")
    }

  } catch (error) {
    console.error(error)
    setResult('Erro ao conectar com o backend.')
  }

  setLoading(false)
}

  return (
    <>
      <nav className="navbar">

  <div className="logo-area">

    <FaSearch className="logo-icon" />

    <h1>JobScope</h1>

  </div>

</nav>

      <section className="hero">
        <h1>Descubra o dia a dia das profissões</h1>

        <p>
          Converse com a IA e descubra como funciona qualquer carreira.
        </p>

        <div className="search-area">
          <input
            type="text"
            placeholder="Ex: Medicina, UX Design, Psicologia..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />

          <button onClick={handleSearch}>
            Pesquisar
          </button>
        </div>
      </section>

      <section className="results">
        {loading && (
          <div className="loading">
            Analisando profissão...
          </div>
        )}

        {result && (
          <div className="ai-card">

  <h2>{search}</h2>

  <div className="content-grid">

    <div className="ai-text">
      <ReactMarkdown>
        {result}
      </ReactMarkdown>
    </div>

    {video && (
      <div className="video-section">

        <h3>
          🎥 Assista ao dia a dia da profissão
        </h3>

        <iframe
          src={video}
          title="Vídeo da profissão"
          allowFullScreen
        />

      </div>
    )}

  </div>

</div>
        )}

      </section>

      <footer className="footer">

  <p>
    © 2026 JobScope • Explore carreiras com IA
  </p>

</footer>

    </>
  )
}

export default App