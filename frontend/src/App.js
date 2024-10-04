// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddCliente from './components/AddCliente';
import AddServico from './components/AddServico';
import ListServicos from './components/ListServicos';
import AddVisita from './components/AddVisita';
import ListPagamentos from './components/ListPagamentos';
import Relatorio from './components/Relatorio';
import ProjecaoGanhos from './components/ProjecaoGanhos';
import ClienteVisitas from './components/ClienteVisitas';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ListServicos />} />
        <Route path="/add_cliente" element={<AddCliente />} />
        <Route path="/add_servico" element={<AddServico />} />
        <Route path="/pagamentos" element={<ListPagamentos />} />
        <Route path="/relatorio" element={<Relatorio />} />
        <Route path="/projecao_ganhos" element={<ProjecaoGanhos />} />
        <Route path="/cliente/:id" element={<ClienteVisitas />} />
        <Route path="/add_visita" element={<AddVisita />} />
      </Routes>
    </Router>
  );
};

export default App;
