// src/components/Relatorio.js

import React, { useState } from 'react';
import { getRelatorio } from '../api';

const Relatorio = () => {
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [visitas, setVisitas] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await getRelatorio(dataInicio, dataFim);
    setVisitas(response.data);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={dataInicio}
          onChange={(e) => setDataInicio(e.target.value)}
          required
        />
        <input
          type="date"
          value={dataFim}
          onChange={(e) => setDataFim(e.target.value)}
          required
        />
        <button type="submit">Gerar Relatório</button>
      </form>

      {visitas.length > 0 && (
        <div>
          <h2>Relatório de Visitas</h2>
          <ul>
            {visitas.map(visita => (
              <li key={visita.id}>
                Cliente ID: {visita.cliente_id} - Serviço ID: {visita.servico_id} - Data: {new Date(visita.data).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Relatorio;
