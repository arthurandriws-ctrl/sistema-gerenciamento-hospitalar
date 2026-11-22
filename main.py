from collections import deque

ARQUIVO = "dados_sistema.txt"

fila_triagem = deque()      # FILA: triagem (FIFO)
pilha_prontuarios = []      # PILHA: prontuários recentes (LIFO), topo = fim da lista
lista_internados = []       # LISTA: pacientes internados
arvore = {}                 # ÁRVORE: dicionários aninhados


# Funções auxiliares de entrada

def ler_texto(msg):
    """Lê um texto não vazio. Troca '|' por '/' para não quebrar o arquivo."""
    while True:
        texto = input(msg).strip()
        if texto:
            return texto.replace("|", "/")
        print("Campo não pode ficar vazio.")


def ler_inteiro(msg):
    """Lê um número inteiro, repetindo até o usuário digitar um válido."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro.")

# FIFO - triagem (inserção no fim, remoção no início)

def fila_inserir():
    paciente = {
        "id": ler_texto("ID do paciente: "),
        "nome": ler_texto("Nome: "),
        "prioridade": ler_texto("Prioridade (ex: Alta/Normal): "),
    }
    fila_triagem.append(paciente)  # entra no FIM da fila
    print("Paciente adicionado à fila.")


def fila_listar():
    if not fila_triagem:
        print("Fila vazia.")
        return
    for pos, p in enumerate(fila_triagem, start=1):
        print(f"{pos}º - {p['id']} | {p['nome']} | {p['prioridade']}")


def fila_atualizar():
    fila_listar()
    if not fila_triagem:
        return
    pos = ler_inteiro("Posição a atualizar: ")
    if 1 <= pos <= len(fila_triagem):
        # Altera os dados, mas a posição na fila permanece a mesma
        fila_triagem[pos - 1]["prioridade"] = ler_texto("Nova prioridade: ")
        print("Atualizado.")
    else:
        print("Posição inválida.")


def fila_remover():
    if not fila_triagem:
        print("Fila vazia.")
        return
    atendido = fila_triagem.popleft()  # sai do INÍCIO da fila
    print(f"Paciente chamado para atendimento: {atendido['nome']}")


# LIFO - prontuários (inserção e remoção no topo)

def pilha_inserir():
    prontuario = {
        "codigo": ler_texto("Código do prontuário: "),
        "paciente": ler_texto("Paciente: "),
        "descricao": ler_texto("Descrição: "),
    }
    pilha_prontuarios.append(prontuario)  # empilha no TOPO
    print("Prontuário empilhado.")


def pilha_listar():
    if not pilha_prontuarios:
        print("Pilha vazia.")
        return
    # reversed: mostra o topo primeiro
    for i, p in enumerate(reversed(pilha_prontuarios)):
        marca = " <- topo" if i == 0 else ""
        print(f"{p['codigo']} | {p['paciente']} | {p['descricao']}{marca}")


def pilha_atualizar():
    if not pilha_prontuarios:
        print("Pilha vazia.")
        return
    pilha_prontuarios[-1]["descricao"] = ler_texto("Nova descrição do prontuário do topo: ")
    print("Topo atualizado.")


def pilha_remover():
    if not pilha_prontuarios:
        print("Pilha vazia.")
        return
    removido = pilha_prontuarios.pop() 
    print(f"Prontuário removido: {removido['codigo']}")


# LISTA - internados (acesso por chave/ID)

def buscar_internado(id_paciente):
    """Retorna o internado com o ID informado ou None."""
    for p in lista_internados:
        if p["id"] == id_paciente:
            return p
    return None


def lista_inserir():
    id_paciente = ler_texto("ID do paciente: ")
    if buscar_internado(id_paciente):
        print("Já existe um internado com esse ID.")
        return
    lista_internados.append({
        "id": id_paciente,
        "nome": ler_texto("Nome: "),
        "leito": ler_texto("Leito: "),
        "estado": ler_texto("Estado (ex: Estavel): "),
    })
    print("Paciente internado.")


def lista_listar():
    if not lista_internados:
        print("Nenhum paciente internado.")
        return
    for p in lista_internados:
        print(f"{p['id']} | {p['nome']} | {p['leito']} | {p['estado']}")


def lista_atualizar():
    p = buscar_internado(ler_texto("ID do paciente: "))
    if p is None:
        print("Paciente não encontrado.")
        return
    p["leito"] = ler_texto("Novo leito: ")
    p["estado"] = ler_texto("Novo estado: ")
    print("Atualizado.")


def lista_remover():
    p = buscar_internado(ler_texto("ID do paciente: "))
    if p is None:
        print("Paciente não encontrado.")
        return
    lista_internados.remove(p)  
    print("Paciente removido (alta).")


# ÁRVORE - dicionários aninhados

def ler_caminho(msg):
    """Converte 'A > B > C' em ['A', 'B', 'C']. Vazio = raiz."""
    texto = input(msg).replace("|", "/")
    return [parte.strip() for parte in texto.split(">") if parte.strip()]


def localizar_no(caminho):
    """Desce pelos dicionários seguindo o caminho. Retorna o nó ou None."""
    no = arvore
    for nome in caminho:
        if nome not in no:
            return None
        no = no[nome]
    return no


def arvore_inserir():
    caminho = ler_caminho("Caminho do pai (ex: Clinica Geral > Cardiologia; vazio = raiz): ")
    pai = localizar_no(caminho)
    if pai is None:
        print("Caminho não encontrado.")
        return
    nome = ler_texto("Nome do novo nó: ")
    if nome in pai:
        print("Esse nó já existe nesse nível.")
        return
    pai[nome] = {}  # novo nó sem filhos
    print("Nó inserido.")


def imprimir_arvore(no, nivel=0):
    for nome, filhos in no.items():
        print("  " * nivel + "- " + nome)
        imprimir_arvore(filhos, nivel + 1)


def arvore_listar():
    if not arvore:
        print("Árvore vazia.")
        return
    imprimir_arvore(arvore)


def arvore_atualizar():
    caminho = ler_caminho("Caminho do nó a renomear (ex: Clinica Geral > Cardiologia): ")
    if not caminho:
        print("Informe um nó.")
        return
    pai = localizar_no(caminho[:-1])
    if pai is None or caminho[-1] not in pai:
        print("Nó não encontrado.")
        return
    novo = ler_texto("Novo nome: ")
    if novo in pai:
        print("Já existe um nó com esse nome nesse nível.")
        return
    pai[novo] = pai.pop(caminho[-1])  # mantém os filhos do nó renomeado
    print("Nó renomeado.")


def arvore_remover():
    caminho = ler_caminho("Caminho do nó a remover: ")
    if not caminho:
        print("Informe um nó.")
        return
    pai = localizar_no(caminho[:-1])
    if pai is None or caminho[-1] not in pai:
        print("Nó não encontrado.")
        return
    del pai[caminho[-1]]  # remove o nó e toda a sua subárvore
    print("Nó (e seus filhos) removido.")


# Persistência em TXT único

def coletar_caminhos(no, prefixo, saida):
    """Recursivamente gera um caminho para cada folha da árvore."""
    for nome, filhos in no.items():
        caminho = prefixo + [nome]
        if filhos:
            coletar_caminhos(filhos, caminho, saida)
        else:
            saida.append(caminho)  # folha: grava o caminho completo


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as arq:
        for p in lista_internados:
            arq.write(f"LISTA|{p['id']}|{p['nome']}|{p['leito']}|{p['estado']}\n")
        for p in fila_triagem:  # ordem da fila preservada
            arq.write(f"FILA|{p['id']}|{p['nome']}|{p['prioridade']}\n")
        for p in pilha_prontuarios:  # da base ao topo, para reconstruir igual
            arq.write(f"PILHA|{p['codigo']}|{p['paciente']}|{p['descricao']}\n")
        caminhos = []
        coletar_caminhos(arvore, [], caminhos)
        for c in caminhos:
            arq.write("ARVORE|" + "|".join(c) + "\n")
    print(f"Dados salvos em {ARQUIVO}.")


def carregar_dados():
    try:
        arq = open(ARQUIVO, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Salve primeiro.")
        return
    # Limpa a memória antes de reconstruir
    lista_internados.clear()
    fila_triagem.clear()
    pilha_prontuarios.clear()
    arvore.clear()
    with arq:
        for linha in arq:
            campos = linha.strip().split("|")
            tipo = campos[0]
            if tipo == "LISTA" and len(campos) == 5:
                lista_internados.append(
                    {"id": campos[1], "nome": campos[2], "leito": campos[3], "estado": campos[4]})
            elif tipo == "FILA" and len(campos) == 4:
                fila_triagem.append(
                    {"id": campos[1], "nome": campos[2], "prioridade": campos[3]})
            elif tipo == "PILHA" and len(campos) == 4:
                pilha_prontuarios.append(
                    {"codigo": campos[1], "paciente": campos[2], "descricao": campos[3]})
            elif tipo == "ARVORE" and len(campos) >= 2:
                no = arvore
                for nome in campos[1:]:
                    no = no.setdefault(nome, {})  # cria o nó se ainda não existir
    print("Dados carregados.")


# Menus

def submenu(titulo, inserir, listar, atualizar, remover):
    while True:
        print(f"\n--- {titulo} ---")
        print("1 - Inserir\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = ler_inteiro("Opção: ")
        match op:
            case 1:
                inserir()
            case 2:
                listar()
            case 3:
                atualizar()
            case 4:
                remover()
            case 0:
                return
            case _:
                print("Opção inválida! Tente novamente.")

def menu_principal():
    while True:
        print("\n" + "=" * 30)
        print("Sistema de Gestão Hospitalar")
        print("=" * 30)
        print("1 - Fila de Triagem")
        print("2 - Pilha de Prontuários")
        print("3 - Pacientes Internados")
        print("4 - Especialidades e Diagnósticos (Árvore)")
        print("5 - Salvar Dados")
        print("6 - Carregar Dados")
        print("0 - Sair")
        op = ler_inteiro("Opção: ")
        match op:
            case 1:
                submenu("Fila de Triagem", fila_inserir, fila_listar, fila_atualizar, fila_remover)
            case 2:
                submenu("Pilha de Prontuários", pilha_inserir, pilha_listar, pilha_atualizar, pilha_remover)
            case 3:
                submenu("Pacientes Internados", lista_inserir, lista_listar, lista_atualizar, lista_remover)
            case 4:
                submenu("Árvore de Especialidades", arvore_inserir, arvore_listar, arvore_atualizar, arvore_remover)
            case 5:
                salvar_dados()
            case 6:
                carregar_dados()
            case 0:
                print("Saindo...")
                return
            case _:
                print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()
