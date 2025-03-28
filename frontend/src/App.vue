<template>
  <div class="container">
    <h1>Busca de Operadoras</h1>
    
    <SearchInput 
      :loading="loading" 
      :search-query="searchQuery" 
      @update:search-query="updateSearchQuery"
    />
    
    <OperadoraTable 
      :results="results" 
      :loading="loading" 
      :search-query="searchQuery" 
      :search-performed="searchPerformed"
    />
  </div>
</template>

<script>
import SearchInput from './components/SearchInput.vue';
import OperadoraTable from './components/OperadoraTable.vue';

export default {
  components: {
    SearchInput,
    OperadoraTable
  },
  data() {
    return {
      searchQuery: '',
      results: [],
      loading: false,
      searchPerformed: false,
      debounceTimeout: null
    }
  },
  methods: {
    updateSearchQuery(query) {
      this.searchQuery = query;
      
      // Limpa o timeout
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }
      
      if (!this.searchQuery || this.searchQuery.length < 1) {
        this.results = [];
        this.searchPerformed = false;
        return;
      }

      // Timeout para debouncing da busca
      this.debounceTimeout = setTimeout(() => {
        this.searchAPI();
      }, 300);
    },
    
    async searchAPI() {
      try {
        this.loading = true;
        this.searchPerformed = true;
        
        const response = await fetch(`http://localhost:5000/api/buscar?q=${(this.searchQuery)}`);
        
        if (!response.ok) {
          throw new Error('Erro na busca');
        }
        
        const data = await response.json();
        this.results = Array.isArray(data) ? data : [data];
      } catch (error) {
        console.error('Erro ao buscar dados:', error);
        this.results = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}
</style>