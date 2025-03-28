from flask import Blueprint, request, jsonify
import pandas as pd
import os
import numpy as np

operadora_bp = Blueprint('operadora', __name__)

csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'downloads', 'Relatorio_cadop.csv')  

try:
    df = pd.read_csv(csv_path, encoding='utf-8', sep=';')
    df = df.replace({np.nan: ''})  
except Exception as e:
    print(f"Erro ao ler o CSV: {e}")
    df = pd.DataFrame()  

@operadora_bp.route('/api/buscar', methods=['GET'])
def buscar_operadoras():
    if df.empty:
        return jsonify({"error": "Erro ao carregar dados do CSV"}), 500

    termo = request.args.get('q', '').lower()  
    if not termo:
        return jsonify({"error": "Informe um termo de busca"}), 400

    if 'Razao_Social' not in df.columns:
        return jsonify({"error": "Coluna 'Razao_Social' não encontrada"}), 400

    resultados = df[df['Razao_Social'].str.lower().str.contains(termo, na=False)]
    return jsonify(resultados.to_dict(orient='records'))
