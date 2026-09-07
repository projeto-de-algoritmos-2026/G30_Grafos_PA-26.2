import streamlit as st
import matplotlib.pyplot as plt
from src.analysis import analyze_components, analyze_department
from src.dataset_loader import load_email_eu_core
from src.kosaraju import KosarajuGraph
from src.visualization import draw_component

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

st.divider()

# Preparar CFCs na mesma ordem usada pelas duas secoes interativas
sccs_sorted = sorted(sccs, key=len, reverse=True)
component_analyses = analyze_components(sccs_sorted, departments)

st.header("Análise por Departamento")

department_options = sorted(set(departments.values()))
selected_department = st.selectbox(
    "Selecione um departamento",
    department_options,
    format_func=lambda department_id: f"Departamento {department_id}",
)

if selected_department is not None:
    department_analysis = analyze_department(
        selected_department,
        component_analyses,
    )

    dept_col1, dept_col2, dept_col3, dept_col4 = st.columns(4)
    with dept_col1:
        st.metric("Pessoas", department_analysis["person_count"])
    with dept_col2:
        st.metric("CFCs em que aparece", len(department_analysis["component_ids"]))
    with dept_col3:
        st.metric(
            "Principal CFC",
            f"CFC #{department_analysis['main_component_id']}",
        )
    with dept_col4:
        st.metric(
            "Membros no principal CFC",
            f"{department_analysis['main_component_percentage']:.1f}%",
        )

    component_labels = ", ".join(
        f"CFC #{component_id}"
        for component_id in department_analysis["component_ids"]
    )
    st.write(f"**Componentes nos quais aparece:** {component_labels}")
    st.write(
        "**Maior concentração:** "
        f"{department_analysis['main_component_person_count']} pessoas no "
        f"CFC #{department_analysis['main_component_id']}"
    )

st.divider()

st.header("Exploração Interativa dos Componentes")

# Opção de seleção do CFC (apresentando o índice e tamanho)
options = [f"CFC #{i} (Tamanho: {len(c)})" for i, c in enumerate(sccs_sorted)]
selected_option = st.selectbox("Selecione um Componente Fortemente Conectado", options)

if selected_option:
    # Extrair o índice a partir da string de opção
    selected_index = options.index(selected_option)
    selected_scc = sccs_sorted[selected_index]
    selected_analysis = component_analyses[selected_index]
    
    st.subheader(f"Análise do CFC Selecionado")
    
    # Calcular métricas
    tamanho = selected_analysis["size"]
    contagem_depts = selected_analysis["department_counts"]
    dept_predominante = selected_analysis["predominant_department"]
    pureza = selected_analysis["predominant_department_percentage"]
    
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.metric("Tamanho", tamanho)
    with colB:
        st.metric("Depts. Presentes", selected_analysis["department_count"])
    with colC:
        st.metric("Dept. Predominante", f"ID {dept_predominante}")
    with colD:
        st.metric("Pureza", f"{pureza:.1f}%")
        
    st.write("**Frequência dos Departamentos neste CFC:**")
    department_frequencies = sorted(
        contagem_depts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    st.write(
        ", ".join(
            f"Dept {department_id}: {count} pessoas"
            for department_id, count in department_frequencies
        )
    )
    
    # Renderizar grafo do componente
    st.write("**Grafo do Componente:**")
    with st.spinner("Desenhando componente..."):
        fig_comp = draw_component(selected_scc, edges, departments)
        st.pyplot(fig_comp)
