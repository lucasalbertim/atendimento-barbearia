// src/components/ListServicos.js

import React, { useEffect, useState } from 'react';
import { getServicos } from '../api';

const ListServicos = () => {
  const [servicos, setServicos] = useState([]);

  useEffect(() => {
    const fetchServicos = async () => {
      const response = await getServicos();
      setServicos(response.data);
    };
    fetchServicos();
  }, []);

  return (
    <div>
      <h2>Serviços</h2>
      <ul>
        {servicos.map(servico => (
          <li key={servico.id}>{servico.nome} - R${servico.preco} ({servico.tempo_estimado} min)</li>
        ))}
      </ul>
    </div>
  );
};

export default ListServicos;
