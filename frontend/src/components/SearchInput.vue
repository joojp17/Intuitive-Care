<template>
    <div class="search-container">
      <input 
        type="text" 
        :value="searchQuery" 
        @input="$emit('update:search-query', $event.target.value)" 
        placeholder="Digite para buscar..."
        class="search-input"
      />
      <div v-if="loading" class="loading-indicator">Buscando...</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      searchQuery: {
        type: String,
        default: ''
      },
      loading: {
        type: Boolean,
        default: false
      }
    },
    emits: ['update:search-query']
  }
  </script>
  
  <style>
  .search-container {
    position: relative;
    margin-bottom: 20px;
  }
  
  .search-input {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .loading-indicator {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #666;
    font-size: 14px;
  }
  </style>