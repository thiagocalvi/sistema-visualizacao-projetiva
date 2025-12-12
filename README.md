# Sistema de Visualização Projetiva

## Introdução
Este projeto implementa um sistema de visualização projetiva utilizando a biblioteca gráfica OpenGL e Pygame. O software permite a renderização de objetos tridimensionais definidos em arquivos de texto, aplicando transformações projetivas com base em parâmetros configuráveis de ponto de vista e plano de projeção.

## Requisitos do Sistema
Para a execução deste software, é necessário um ambiente Python 3 configurado. As dependências externas estão listadas no arquivo `requirements.txt` e incluem:

*   pygame (versão 2.6.1)
*   PyOpenGL (versão 3.1.10)

## Instalação
Recomenda-se a utilização de um ambiente virtual para o isolamento das dependências. Para instalar as bibliotecas necessárias, execute o seguinte comando no terminal:

```bash
pip install -r requirements.txt
```

## Execução
O programa pode ser iniciado através do script principal `main.py`. O arquivo de objeto a ser carregado pode ser especificado como um argumento de linha de comando. Caso nenhum argumento seja fornecido, o sistema carregará o arquivo `cube.txt` por padrão.

### Comando Básico
```bash
python main.py [caminho_do_arquivo_objeto]
```

### Exemplos
```bash
python main.py tetrahedron.txt
python main.py cube.txt
```

### Controles
Durante a execução, as seguintes teclas podem ser utilizadas para manipular a posição do centro de projeção (C):

*   **W / S**: Movimentação no eixo Z (aproximar/afastar).
*   **A / D**: Movimentação no eixo X (esquerda/direita).
*   **Q / E**: Movimentação no eixo Y (cima/baixo).
*   **ESC**: Encerrar a aplicação.

## Formato dos Arquivos

### Arquivo de Objeto
O arquivo que descreve o objeto tridimensional deve seguir estritamente a estrutura definida abaixo. O arquivo é composto por duas seções principais: vértices e faces.

1.  **Número de Vértices**: A primeira linha contém um número inteiro $N_v$ representando a quantidade total de vértices.
2.  **Lista de Vértices**: As $N_v$ linhas subsequentes contêm as coordenadas $x, y, z$ de cada vértice, separadas por espaço.
3.  **Número de Faces**: Após a lista de vértices, uma linha contém um número inteiro $N_f$ representando a quantidade de faces (superfícies).
4.  **Lista de Faces**: As $N_f$ linhas seguintes descrevem cada face. Cada linha inicia com o número de vértices que compõem aquela face, seguido pelos índices dos vértices (baseados na ordem de declaração, iniciando em 0).

**Exemplo (Tetraedro):**
```text
4
1.0 1.0 1.0
1.0 -1.0 -1.0
-1.0 1.0 -1.0
-1.0 -1.0 1.0
4
3 0 1 2
3 0 3 1
3 0 2 3
3 1 3 2
```

### Arquivo de Configuração (config.txt)
O sistema permite a configuração dos parâmetros projetivos através do arquivo `config.txt`. Este arquivo define o Centro de Projeção (C) e os três pontos que definem o Plano de Projeção (P1, P2, P3).

Cada linha do arquivo deve iniciar com o identificador do parâmetro, seguido pelas coordenadas $x, y, z$.

*   **C**: Centro de Projeção (Ponto de vista).
*   **P1, P2, P3**: Pontos não colineares que definem o plano onde o objeto será projetado.

**Exemplo de Configuração:**
```text
C 0 0 40
P1 -1 -1 0
P2 1 -1 0
P3 0 1 0
```
