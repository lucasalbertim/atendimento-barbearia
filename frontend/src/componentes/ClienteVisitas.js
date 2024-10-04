// src/components/ClienteVisitas.js

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getClientes } from '../api';

const ClienteVisitas = () => {
  const { id } = useParams();
  const [cliente, setCliente] = useState(null);
  const [totalVisitas, setTotalVisitas] = useState(0);

  useEffect(() => {
    const fetchCliente = async () => {
      const response = await getClientes();
      const clienteData = response.data.find(c => c.id === parseInt(id));
      setCliente(clienteData);
      setTotalVisitas(clienteData.visitas.length); // Supondo que a contagem de visitas está disponível aqui
    };
    fetchCliente();
  }, [id]);

  if (!cliente) return <div>Carregando...</div>;

  return (
    <div>
      <h2>Visitas de {cliente.nome}</h2>
      <p>Total de Visitas: {totalVisitas}</p>
      {/* Aqui você pode adicionar mais informações ou detalhes sobre as visitas */}
    </div>
  );
};

export default ClienteVisitas;
