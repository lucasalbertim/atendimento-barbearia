// src/components/AddCliente.js

import React, { useState } from 'react';
import { addCliente } from '../api';

const AddCliente = () => {
  const [nome, setNome] = useState('');
  const [cpf, setCpf] = useState('');
  const [telefone, setTelefone] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addCliente({ nome, cpf, telefone });
    setNome('');
    setCpf('');
    setTelefone('');
    // Redirecionar ou exibir mensagem de sucesso
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Nome" value={nome} onChange={(e) => setNome(e.target.value)} required />
      <input type="text" placeholder="CPF" value={cpf} onChange={(e) => setCpf(e.target.value)} required />
      <input type="text" placeholder="Telefone" value={telefone} onChange={(e) => setTelefone(e.target.value)} required />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default AddCliente;
