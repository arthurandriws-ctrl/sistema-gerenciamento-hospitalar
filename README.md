# Sistema de Gestão Hospitalar

Projeto final da disciplina **Teoria das Estruturas de Dados**.
Sistema em Python, executado pelo terminal (CLI), que integra **Fila, Pilha, Lista e Árvore** para simular o núcleo lógico de um sistema hospitalar, com persistência em arquivo texto.

---

## 1. Como executar

**Requisitos:** Python 3.10 ou superior (o programa usa a instrução `match/case`). Nenhuma biblioteca externa é necessária.

```bash
python main.py
```

(em alguns sistemas, `python3 main.py`)

O sistema inicia **totalmente vazio**. Para guardar o que foi cadastrado, use a opção **5 - Salvar Dados**, que cria o arquivo `dados_sistema.txt`. Em uma execução futura, use **6 - Carregar Dados** para restaurar tudo.

### Roteiro rápido de teste

1. Menu `1` (Fila de Triagem) → `1` Inserir → cadastre alguns pacientes → `2` Listar.
2. Menu `2` (Pilha) → insira prontuários e liste (o topo aparece marcado).
3. Menu `3` (Internados) → cadastre pacientes e leitos.
4. Menu `4` (Árvore) → insira uma especialidade (caminho vazio = raiz), depois filhos usando o caminho, por exemplo `Clinica Geral > Cardiologia`.
5. Menu `5` para salvar, feche o programa, abra novamente e use `6` para carregar.

---

## 2. Visão geral do funcionamento

O programa tem um **menu principal** com seis opções de trabalho e a saída:

| Opção | Ação |
|-------|------|
| 1 | Fila de Triagem |
| 2 | Pilha de Prontuários |
| 3 | Pacientes Internados (Lista) |
| 4 | Especialidades e Diagnósticos (Árvore) |
| 5 | Salvar Dados |
| 6 | Carregar Dados |
| 0 | Sair |

As opções 1 a 4 abrem um **submenu CRUD** idêntico em formato: Inserir, Listar, Atualizar, Remover e Voltar. Cada estrutura tem suas próprias funções, que respeitam as regras conceituais dela.

Todos os dados ficam em memória em quatro variáveis globais. O arquivo só é lido ou escrito quando o usuário escolhe Salvar ou Carregar.

| Estrutura | Variável | Tipo Python | Papel no hospital |
|-----------|----------|-------------|-------------------|
| Fila | `fila_triagem` | `collections.deque` | Ordem de atendimento na triagem |
| Pilha | `pilha_prontuarios` | `list` | Prontuários acessados recentemente |
| Lista | `lista_internados` | `list` | Pacientes internados e leitos |
| Árvore | `arvore` | `dict` aninhado | Especialidades e diagnósticos |

---

## 3. Justificativa técnica das estruturas

### Fila (FIFO) - Triagem de pacientes
Na triagem, o paciente que chegou primeiro deve ser atendido primeiro. Isso é exatamente o comportamento FIFO (*First In, First Out*): a inserção ocorre sempre no fim e a remoção sempre no início. Usamos `collections.deque` porque `popleft()` remove do início em tempo O(1), enquanto `list.pop(0)` seria O(n), pois desloca todos os elementos restantes. Em um hospital com muitos pacientes, essa diferença importa.

### Pilha (LIFO) - Histórico de prontuários recentes
Quem revisa prontuários normalmente quer voltar ao último que abriu, depois ao anterior, e assim por diante, como o botão "voltar" de um navegador. Isso é o comportamento LIFO (*Last In, First Out*). Usamos `list` com `append()` (empilhar) e `pop()` (desempilhar), ambos O(1) no fim da lista, que funciona como o topo.

### Lista - Pacientes internados
Os internados não seguem ordem de atendimento: é preciso consultar, alterar leito ou estado e dar alta a **qualquer** paciente, a qualquer momento. A lista permite acesso e remoção de qualquer elemento, por busca de ID. É a estrutura adequada para um cadastro dinâmico que cresce e diminui sem regra de ordem.

### Árvore - Especialidades médicas e diagnósticos
Especialidades e diagnósticos são naturalmente hierárquicos (especialidade → subespecialidade → diagnóstico). Uma estrutura linear não representaria essa relação de "pertence a". A árvore permite navegar do geral para o específico. Como o Python não tem árvore nativa, foi usado **dicionário aninhado**, em que cada chave é um nó e o valor é um dicionário com os filhos.

---

## 4. Como cada estrutura foi implementada

### 4.1 Fila (`deque`)

```python
fila_triagem = deque()
```

Cada paciente é um dicionário `{"id", "nome", "prioridade"}`.

| Operação | Função | Implementação |
|----------|--------|---------------|
| Inserir | `fila_inserir()` | `fila_triagem.append(paciente)` adiciona no **fim** |
| Listar | `fila_listar()` | percorre com `enumerate`, mostrando a posição (1º, 2º, ...) |
| Atualizar | `fila_atualizar()` | acessa pela posição e altera a prioridade, **sem mudar a ordem** |
| Remover | `fila_remover()` | `fila_triagem.popleft()` remove e retorna o **primeiro** (paciente chamado) |

A regra "insere no fim, remove no início" é garantida pelo fato de só existirem essas duas funções de entrada e saída.

### 4.2 Pilha (`list`)

```python
pilha_prontuarios = []
```

Cada prontuário é um dicionário `{"codigo", "paciente", "descricao"}`. O **topo é o último elemento** da lista.

| Operação | Função | Implementação |
|----------|--------|---------------|
| Inserir (empilhar) | `pilha_inserir()` | `pilha_prontuarios.append(prontuario)` |
| Listar | `pilha_listar()` | `reversed(...)` mostra do topo para a base e marca o topo |
| Atualizar | `pilha_atualizar()` | altera somente `pilha_prontuarios[-1]` (o topo) |
| Remover (desempilhar) | `pilha_remover()` | `pilha_prontuarios.pop()` remove o topo |

Em uma pilha só o topo é acessível, por isso a atualização é restrita a ele.

### 4.3 Lista (`list`)

```python
lista_internados = []
```

Cada internado é um dicionário `{"id", "nome", "leito", "estado"}`.

| Operação | Função | Implementação |
|----------|--------|---------------|
| Buscar | `buscar_internado(id)` | percorre a lista comparando o ID; retorna o registro ou `None` |
| Inserir | `lista_inserir()` | recusa ID repetido e faz `append()` |
| Listar | `lista_listar()` | percorre e imprime todos |
| Atualizar | `lista_atualizar()` | localiza pelo ID e altera leito e estado |
| Remover | `lista_remover()` | localiza pelo ID e usa `remove()` (alta hospitalar) |

### 4.4 Árvore (dicionários aninhados)

```python
arvore = {}
```

Exemplo de conteúdo em memória:

```python
{
  "Clinica Geral": {
      "Cardiologia": {"Arritmia": {}},
      "Ortopedia":   {"Fratura": {}}
  }
}
```

- Cada **chave** é o nome de um nó.
- Cada **valor** é outro dicionário com os filhos daquele nó.
- Um dicionário vazio `{}` indica um nó **folha**.
- A **raiz** é o próprio dicionário `arvore` (pode ter várias especialidades no primeiro nível).

O usuário informa a posição de um nó como um **caminho**, por exemplo `Clinica Geral > Cardiologia`.

| Função | O que faz |
|--------|-----------|
| `ler_caminho()` | transforma o texto `"A > B > C"` na lista `["A", "B", "C"]` (vazio = raiz) |
| `localizar_no(caminho)` | começa em `arvore` e desce uma chave por vez; retorna o dicionário do nó ou `None` se o caminho não existir |
| `arvore_inserir()` | localiza o pai e cria o filho com `pai[nome] = {}` |
| `imprimir_arvore()` | **recursiva**: imprime o nome, depois chama a si mesma para os filhos com um nível a mais de indentação |
| `arvore_listar()` | chama `imprimir_arvore(arvore)` |
| `arvore_atualizar()` | renomeia um nó com `pai[novo] = pai.pop(antigo)`, preservando os filhos |
| `arvore_remover()` | `del pai[nome]` remove o nó **e toda a sua subárvore** |

---

## 5. Persistência em arquivo texto

Todo o estado é gravado em **um único arquivo**, `dados_sistema.txt`, sem banco de dados, JSON, CSV ou `pickle`. Cada linha começa com um **identificador** da estrutura e os campos são separados por **pipe (`|`)**:

```
LISTA|101|Carlos Silva|Leito 04|Estavel
FILA|205|Roberto Alves|Prioridade Alta
PILHA|PRONT-889|Paciente 101|Consulta Cardiologia
ARVORE|Clinica Geral|Cardiologia|Arritmia
```

### Salvar (`salvar_dados`)
- Abre o arquivo em modo escrita (`"w"`), sobrescrevendo o conteúdo anterior.
- Grava `LISTA`, `FILA` (na ordem atual da fila) e `PILHA` (da **base ao topo**, para que ao recarregar o topo continue sendo o último elemento).
- Para a árvore, a função recursiva `coletar_caminhos` gera um caminho para cada **folha**; cada caminho vira uma linha `ARVORE|...`. Como todo nó pertence a algum caminho até uma folha, a árvore inteira é preservada.

### Carregar (`carregar_dados`)
- Se o arquivo não existir, avisa o usuário e não altera nada.
- Esvazia as estruturas em memória e lê o arquivo linha a linha.
- Separa cada linha com `split("|")` e usa o primeiro campo para decidir em qual estrutura inserir.
- Para `ARVORE`, desce pelos nomes usando `setdefault`, que cria o nó caso ainda não exista e reaproveita nós já criados por outras linhas.

### Proteção do delimitador
A função `ler_texto` troca qualquer `|` digitado pelo usuário por `/`, evitando que o texto quebre o formato do arquivo.

---

## 6. Organização do código (`main.py`)

O arquivo está dividido em blocos, cada um com funções de responsabilidade única:

1. **Estruturas em memória**: as quatro variáveis globais (iniciam vazias).
2. **Funções de entrada**: `ler_texto` (texto não vazio) e `ler_inteiro` (repete até receber um número válido, evitando erro com entradas inválidas).
3. **Fila**: `fila_inserir`, `fila_listar`, `fila_atualizar`, `fila_remover`.
4. **Pilha**: `pilha_inserir`, `pilha_listar`, `pilha_atualizar`, `pilha_remover`.
5. **Lista**: `buscar_internado`, `lista_inserir`, `lista_listar`, `lista_atualizar`, `lista_remover`.
6. **Árvore**: `ler_caminho`, `localizar_no`, `arvore_inserir`, `imprimir_arvore`, `arvore_listar`, `arvore_atualizar`, `arvore_remover`.
7. **Persistência**: `coletar_caminhos`, `salvar_dados`, `carregar_dados`.
8. **Menus**: `submenu` e `menu_principal`.

### Fluxo de execução

1. `if __name__ == "__main__"` chama `menu_principal()`.
2. O menu principal roda em um laço `while True`, lê a opção com `ler_inteiro` e usa `match/case` para escolher a ação.
3. As opções 1 a 4 chamam `submenu`, que recebe como argumentos as **quatro funções** (inserir, listar, atualizar, remover) da estrutura escolhida. Assim, um único submenu serve para as quatro estruturas, sem repetir código.
4. A opção `0` encerra o laço e finaliza o programa. Opções inválidas exibem uma mensagem e o menu é mostrado novamente.

---

## 7. Resumo

O sistema mantém quatro estruturas em memória: uma **fila** (`deque`) para a triagem, uma **pilha** (`list`) para os prontuários recentes, uma **lista** (`list`) para os internados e uma **árvore** (dicionários aninhados) para especialidades e diagnósticos. O usuário opera todas por menus numéricos com CRUD completo, respeitando as regras de cada estrutura: fila insere no fim e remove no início, pilha opera só no topo, lista acessa por ID e árvore navega por caminhos hierárquicos. Os dados são salvos e carregados explicitamente em um único arquivo `dados_sistema.txt`, com um identificador por linha e campos separados por `|`.
