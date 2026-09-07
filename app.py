import streamlit as st
import matplotlib.pyplot as plt
from src.dataset_loader import load_email_eu_core
from src.kosaraju import KosarajuGraph

st.set_page_config(page_title="Análise de CFCs", layout="wide")

@st.cache_data
def load_and_process_data():
    edges, departments = load_email_eu_core()
    
    # Montar grafo
    vertices = list(departments.keys())
    graph = KosarajuGraph(vertices)
    for u, v in edges:
        graph.add_edge(u, v)
        
    sccs = graph.get_sccs()
    
    return edges, departments, sccs

st.title("Dashboard de Análise: Componentes Fortemente Conectados")

edges, departments, sccs = load_and_process_data()

st.header("Métricas Gerais")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pessoas", len(departments))
with col2:
    st.metric("Relações", len(edges))
with col3:
    st.metric("Departamentos", len(set(departments.values())))
    
st.subheader("Resultados do Algoritmo de Kosaraju")
col4, col5 = st.columns(2)
with col4:
    st.metric("Qtd. de CFCs Encontrados", len(sccs))

scc_sizes = [len(c) for c in sccs]
max_scc = max(scc_sizes) if scc_sizes else 0

with col5:
    st.metric("Tamanho do Maior CFC", max_scc)

st.subheader("Distribuição dos Tamanhos dos Componentes")

fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(scc_sizes, bins=50, color='skyblue', edgecolor='black')
ax.set_yscale('log')
ax.set_xlabel("Tamanho do CFC")
ax.set_ylabel("Frequência (escala log)")
ax.set_title("Histograma de Distribuição de Tamanho dos CFCs")
st.pyplot(fig)
