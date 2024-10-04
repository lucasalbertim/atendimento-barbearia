// src/components/ProjecaoGanhos.js

import React, { useEffect, useState } from 'react';
import { getProjecaoGanhos } from '../api';

const ProjecaoGanhos = () => {
  const [totalGanho, setTotalGanho] = useState(0);
  const [projecaoMensal, setProjecaoMensal] = useState(0);

  useEffect(() => {
    const fetchProjecao = async () => {
      const response = await getProjecaoGanhos();
      setTotalGanho(response.data.total_ganho);
      setProjecaoMensal(response.data.projecao_mensal);
    };
    fetchProjecao();
  }, []);

  return (
    <div>
      <h2>Projeção de Ganhos</h2>
      <p>Total Ganho: R${totalGanho.toFixed(2)}</p>
      <p>Projeção Mensal: R${projecaoMensal.toFixed(2)}</p>
    </div>
  );
};

export default ProjecaoGanhos;
