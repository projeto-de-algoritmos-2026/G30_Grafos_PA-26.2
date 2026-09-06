# Identificador de Componentes Fortemente Conectados

**Número da Lista**: 1<br>
**Conteúdo da Disciplina**: Grafos<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| XX/XXXXXXX | Tiago Antunes |
| 23/1026714 | Euller Júlio da Silva |

## Apresentação do trabalho
[Link para o vídeo de apresentação](https://youtu.be/)

## Sobre
O presente projeto consiste na análise de conexões em um grafo direcionado para identificar grupos de entidades onde todas estão mutuamente interconectadas. Este tipo de análise estrutural é fundamental para o entendimento de redes complexas, permitindo descobrir ciclos e dependências que formam a base do sistema estudado.

Os dados utilizados (dataset) representam as relações direcionadas do problema modelado. Eles consistem em vértices (entidades) e arestas direcionadas (conexões de uma entidade para outra). O dataset foi escolhido para proporcionar uma estrutura rica o suficiente, garantindo que o tempo de execução e a corretude dos algoritmos sobre grafos possam ser validados em um cenário não trivial.

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
