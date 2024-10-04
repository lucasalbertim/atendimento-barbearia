// src/components/AddServico.js

import React, { useState } from 'react';
import { addServico } from '../api';

const AddServico = () => {
  const [nome, setNome] = useState('');
  const [preco, setPreco] = useState('');
  const [tempoEstimado, setTempoEstimado] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addServico({ nome, preco, tempo_estimado: tempoEstimado });
    setNome('');
    setPreco('');
    setTempoEstimado('');
    // Redirecionar ou exibir mensagem de sucesso
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Nome" value={nome} onChange={(e) => setNome(e.target.value)} required />
      <input type="number" placeholder="Preço" value={preco} onChange={(e) => setPreco(e.target.value)} required />
      <input type="number" placeholder="Tempo Estimado (min)" value={tempoEstimado} onChange={(e) => setTempoEstimado(e.target.value)} required />
      <button type="submit">Adicionar Serviço</button>
    </form>
  );
};

export default AddServico;
