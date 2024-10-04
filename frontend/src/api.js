// src/api.js

import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Altere se necessário

export const getClientes = () => {
  return axios.get(`${API_URL}/`);
};

export const addCliente = (cliente) => {
  return axios.post(`${API_URL}/add_cliente`, cliente);
};

export const getServicos = () => {
  return axios.get(`${API_URL}/servicos`);
};

export const addServico = (servico) => {
  return axios.post(`${API_URL}/add_servico`, servico);
};

export const getPagamentos = () => {
  return axios.get(`${API_URL}/pagamentos`);
};

export const addVisita = (visita) => {
  return axios.post(`${API_URL}/add_visita`, visita);
};

export const getRelatorio = (dataInicio, dataFim) => {
  return axios.post(`${API_URL}/relatorio`, { data_inicio: dataInicio, data_fim: dataFim });
};

export const getProjecaoGanhos = () => {
  return axios.get(`${API_URL}/projecao_ganhos`);
};

// Continue com outras funções conforme necessário
