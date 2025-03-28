<template>
    <div>
      <div v-if="results.length > 0" class="results-container">
        <h2>Resultados</h2>
        <div v-for="(item, index) in results" :key="index" class="result-item">
          <h3>{{ item.Razao_Social }}</h3>
          <div class="result-details">
            <div class="detail-row">
              <span class="detail-label">Registro ANS:</span>
              <span class="detail-value">{{ item.Registro_ANS }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">CNPJ:</span>
              <span class="detail-value">{{ formatCNPJ(item.CNPJ) }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Modalidade:</span>
              <span class="detail-value">{{ item.Modalidade }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Endereço:</span>
              <span class="detail-value">
                {{ item.Logradouro }}, {{ item.Numero }}
                {{ item.Complemento ? ', ' + item.Complemento : '' }}, 
                {{ item.Bairro }}, {{ item.Cidade }} - {{ item.UF }}, 
                CEP: {{ formatCEP(item.CEP) }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Contato:</span>
              <span class="detail-value">
                Tel: {{ formatPhone(item.DDD, item.Telefone) }}
                {{ item.Fax ? ' | Fax: ' + formatPhone(item.DDD, item.Fax) : '' }}
              </span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ item.Endereco_eletronico }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Representante:</span>
              <span class="detail-value">{{ item.Representante }} ({{ item.Cargo_Representante }})</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else-if="searchQuery && !loading && searchPerformed" class="no-results">
        Nenhum resultado encontrado para "{{ searchQuery }}"
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      results: {
        type: Array,
        default: () => []
      },
      loading: {
        type: Boolean,
        default: false
      },
      searchQuery: {
        type: String,
        default: ''
      },
      searchPerformed: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      formatCNPJ(cnpj) {
        if (!cnpj) return 'N/A';
        
        const cnpjStr = cnpj.toString().padStart(14, '0');
        return `${cnpjStr.slice(0, 2)}.${cnpjStr.slice(2, 5)}.${cnpjStr.slice(5, 8)}/${cnpjStr.slice(8, 12)}-${cnpjStr.slice(12)}`;
      },
      
      formatCEP(cep) {
        if (!cep) return 'N/A';
        
        const cepStr = cep.toString().padStart(8, '0');
        return `${cepStr.slice(0, 5)}-${cepStr.slice(5)}`;
      },
      
      formatPhone(ddd, phone) {
        if (!ddd || !phone) return 'N/A';
        
        const dddStr = ddd.toString().replace('.0', '');
        const phoneStr = phone.toString().replace('.0', '');
        
        return `(${dddStr}) ${phoneStr}`;
      }
    }
  }
  </script>
  
  <style>
  .results-container {
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 15px;
    background-color: #f9f9f9;
  }
  
  .result-item {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 15px;
  }
  
  .result-item h3 {
    margin-top: 0;
    color: #2c3e50;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
  }
  
  .result-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  .detail-row {
    display: flex;
    flex-wrap: wrap;
  }
  
  .detail-label {
    font-weight: bold;
    min-width: 120px;
    color: #555;
  }
  
  .detail-value {
    flex: 1;
  }
  
  .no-results {
    padding: 20px;
    text-align: center;
    background-color: #f8f8f8;
    border: 1px solid #eee;
    border-radius: 4px;
    color: #666;
  }
  
  @media (max-width: 600px) {
    .detail-row {
      flex-direction: column;
    }
    
    .detail-label {
      margin-bottom: 4px;
    }
  }
  </style>