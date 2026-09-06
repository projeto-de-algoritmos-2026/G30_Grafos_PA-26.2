# Identificador de Componentes Fortemente Conectados

**Número da Lista**: 1<br>
**Conteúdo da Disciplina**: Grafos<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 23/1011838 | Tiago Antunes Balieiro |
| 23/1026714 | Euller Júlio da Silva |

## Apresentação do trabalho
[Link para o vídeo de apresentação](https://youtu.be/)

## Sobre
O presente projeto consiste na análise de conexões em um grafo direcionado para identificar grupos de entidades onde todas estão mutuamente interconectadas. Este tipo de análise estrutural é fundamental para o entendimento de redes complexas, permitindo descobrir ciclos e dependências que formam a base do sistema estudado.



O projeto utiliza a base pública **email-Eu-core Network**, disponibilizada pelo Stanford Network Analysis Project (SNAP). O dataset representa a rede de comunicação por e-mails de uma grande instituição de pesquisa europeia, com os dados anonimizados para preservar a identidade dos participantes. Cada pessoa da instituição é modelada como um vértice de um grafo direcionado, e uma aresta `u → v` existe quando a pessoa `u` enviou pelo menos um e-mail para a pessoa `v`. A base utilizada contém **1.005 vértices e 25.571 relações**, além de informações adicionais de comunidade, nas quais cada indivíduo está associado a exatamente um dos **42 departamentos** da instituição. Essas informações permitem analisar não apenas a estrutura da rede de comunicação, mas também investigar a relação entre os Componentes Fortemente Conectados encontrados e a organização departamental da instituição.

- Fonte dos dados: https://snap.stanford.edu/data/email-Eu-core.html

O objetivo principal deste trabalho é modelar o dataset na forma de um grafo direcionado e extrair informações valiosas a partir dele. Mais especificamente, busca-se implementar um algoritmo eficiente para mapear as interações fechadas na rede e compreender os subgrupos existentes, aplicando na prática os conceitos teóricos de grafos.

Para isso, a abordagem baseada em **Componentes Fortemente Conectados (CFC)** é justificada por permitir particionar a rede em agrupamentos (clusters) em que cada par de vértices tem um caminho mútuo. Identificar esses CFCs ajuda a entender o núcleo de relacionamentos da rede, simplificar o processamento através do grafo condensado e resolver as dependências do problema original de maneira eficiente.

Para a extração dos componentes, optou-se pela utilização do **Algoritmo de Kosaraju**. A escolha baseia-se na sua elegância e facilidade de implementação, que utiliza essencialmente duas chamadas de Busca em Profundidade (DFS): uma no grafo original para determinar a ordem de finalização dos vértices e outra no grafo transposto (reverso). O algoritmo executa em tempo linear $O(V + E)$, sendo eficiente e perfeitamente adequado para processar o dataset escolhido dentro dos requisitos de tempo e espaço computacional.

## Screenshots
A seguir estão imagens do projeto em funcionamento.

![Screenshot 1](/docs/screenshot1.png)
*Figura 1: Descrição da interface ou visualização do terminal.*

## Instalação
**Linguagem**: Python<br>
**Pré-requisitos:** Python 3.10+ instalado<br>

### Como rodar

1. Clonar o repositório para a sua máquina
```bash
git clone https://github.com/projeto-de-algoritmos-2026/G30_Grafos_PA-26.2.git
```

2. Navegar até o diretório do projeto
```bash
cd G30_Grafos_PA-26.2
```

3. Instalar as dependências
```bash
python -m pip install -r requirements.txt
```

4. Executar a aplicação
```bash
python src/main.py
```

## Uso
Após iniciar o projeto, o usuário poderá visualizar os componentes fortemente conectados extraídos da rede por meio do algoritmo de Kosaraju. (Detalhar aqui futuramente os passos exatos de interação com a aplicação, entrada de dados e interpretação dos resultados).
