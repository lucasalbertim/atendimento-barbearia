// src/components/AddVisita.js

import React, { useEffect, useState } from 'react';
import { getClientes, getServicos, addVisita } from '../api';

const AddVisita = () => {
  const [clientes, setClientes] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [clienteId, setClienteId] = useState('');
  const [servicoId, setServicoId] = useState('');

  useEffect(() => {
    const fetchClientes = async () => {
      const response = await getClientes();
      setClientes(response.data);
    };
    const fetchServicos = async () => {
      const response = await getServicos();
      setServicos(response.data);
    };

    fetchClientes();
    fetchServicos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addVisita({ cliente_id: clienteId, servico_id: servicoId });
    // Redirecionar ou exibir mensagem de sucesso
  };

  return (
    <form onSubmit={handleSubmit}>
      <select value={clienteId} onChange={(e) => setClienteId(e.target.value)} required>
        <option value="">Selecione um Cliente</option>
        {clientes.map(cliente => (
          <option key={cliente.id} value={cliente.id}>{cliente.nome}</option>
        ))}
      </select>

      <select value={servicoId} onChange={(e) => setServicoId(e.target.value)} required>
        <option value="">Selecione um Serviço</option>
        {servicos.map(servico => (
          <option key={servico.id} value={servico.id}>{servico.nome}</option>
        ))}
      </select>

      <button type="submit">Adicionar Visita</button>
    </form>
  );
};

export default AddVisita;
