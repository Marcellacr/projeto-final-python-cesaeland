import json
import time

# Carregar os ficheiros JSON
with open("Cesaeland_logins.json", "r") as f:
    logins = json.load(f)

with open("Cesaeland_atracoes.json", "r") as f:
    atracoes = json.load(f)    

with open("Cesaeland_vendas.json", "r") as f:
    vendas = json.load(f)     

with open("Cesaeland_custos.json", "r") as f:
    custos = json.load(f)    

#Função para gravar novos logins
def gravar_login():
    json_str = json.dumps(logins)
    with open("Cesaeland_logins.json", "w") as arquivo:
        arquivo.write(json_str)

#Função para encontrar um usuário
def find_usuario(user_name):
    for login in logins:
        if login['username'] == user_name:
            return True

    return False
    
#Função para adicionar um novo logins
def adicionar_login():
    nome_usuario = input("Insira o nome do novo usuario: ")
    
    while True:
        if find_usuario(nome_usuario) == True:
         print("O nome escolhido já está em uso.")
         nome_usuario = input("Escolha outro usuário ou digite 0 para sair: ")
         if(nome_usuario == 0 or nome_usuario == '0'):
            return
        else:
            break

    password_valid = False
    password = input("Insira a password: ")
    password_conf = input("Confirme a sua password ou digite 0 para sair: ")
    while(password_valid == False):
        if(password_conf == 0 or password_conf == '0'):
            return
        elif(password == password_conf):
            password_valid = True
            break

        password_conf = input("Tente novamente! Insira a password ou 0 para sair: ")

    print("\nEscolha o role do novo usuário")
    print("1. Administrador")
    print("2. Engenheiro de Manutenção")
    print("----------------------------------------")

    role = input("Escolha uma das opções: ")    


    if role == "1":
        role = "ADMIN"
    if role == "2":
        role = "ENG"        

    novo_login = {
        "role": role,
        "username": nome_usuario,
        "password": password,
    }

    logins.append(novo_login)
    gravar_login()
    print("Novo login adicionado com sucesso!\n")

# Função para fazer o login
def login():
    role = None
    user = input("Insira o nome de usuario: ")
    password = input("Insira a password: ")

    for login in logins:
        if (login['username'] == user and login['password'] == password):
            role = login['role']
            break
    if role:
        print(f"Login efetuado com sucesso como {role}")
    else:
        print("Usuario ou password incorretos.")
    return role


# Funções para os consultar as atrações disponiveis 
def consultar_atracoes_disponiveis():
        imprimir_atracoes(atracoes)

#Função para achar a atração mais vendida, consequentemente a mais procurada
def atracao_mais_vendida(tipo_cliente):

    atracoes_recorrencias = {}
    vendas_atracoes_ids = []
    for item in vendas:
          if item['tipoCliente'].lower() == tipo_cliente.lower():
            vendas_atracoes_ids.append(item['atracao'])
    
    for item in vendas:
           if item['tipoCliente'].lower() == tipo_cliente.lower():
               atracoes_recorrencias[item['atracao']] = vendas_atracoes_ids.count(item['atracao'])

    mais_vendida = max(atracoes_recorrencias, key=atracoes_recorrencias.get)

    for item in atracoes:
        if item['id'] == mais_vendida:
           return item        


#Função para descobrir uma atração
def find_atracao(id_atracao):
     for atracao in atracoes:
        if atracao['id'] == id_atracao:
            return atracao

#Função para saber qual a atração que dá mais lucro
def atracao_lucro(tipo):

    atracao_lucro = {}
    
    for atracao in atracoes:
        count = 0
        for venda in vendas:
            if venda['atracao'] == atracao['id']:
                if venda['tipoCliente'] == 'adulto':
                    count += atracao['precoAdulto']
                else:
                    count += atracao['precoCrianca']
        
        custo_total = custo_total_atracao(atracao)
        atracao_lucro[atracao['id']] = count - custo_total
           
    atracao_id = 0
    if(tipo == 'max'):
        atracao_id = max(atracao_lucro, key=atracao_lucro.get)
    else:
        atracao_id = min(atracao_lucro, key=atracao_lucro.get)
    
    return {"id": atracao_id, "valor_total": atracao_lucro[atracao_id]}

#Função para saber o total de vendas de uma atração
def total_vendas():
    total = 0
    for item in vendas:
        atracao = find_atracao(item['atracao'])
        if item['tipoCliente'] == 'adulto':
             total += atracao['precoAdulto']
        else:
             total += atracao['precoCrianca']
    return total

#Função para saber o total dos custos do Parque Cesaeland
def custo_atracao(atracao): 
    for custo in custos:
        if atracao['id'] == custo['atracao']:
            return custo
        
#Função para calcular o custo por bilhete      
def custo_por_bilhetes(atracao):
    atracoes_rec = atracoes_recorrencia()
    custo = custo_atracao(atracao)
    if custo != None:
        return custo['custoManutencaoBilhete'] * atracoes_rec[atracao['id']]
    return custo

#Função para calcular o custo total das atrações
def custo_total_atracao(atracao): 
    custo = custo_atracao(atracao)
    if custo != None:
         return custo_por_bilhetes(atracao) + custo['custoFixoMes']
    return 0
        
# Função custo total do parque
def total_custos():
    count = 0
    for atracao in atracoes:
        count += custo_total_atracao(atracao)
    return count     

#Transformar segundos em minutos
def duracao(segundos): 
    horas = segundos // 3600
    minutos = (segundos // 60) - (horas * 60)
    segundos = segundos - (horas * 3600) - (minutos * 60)
    return f"{minutos} min : {segundos}s"
   
   
#Funções para imprimir as atrações de diferentes maneiras: por linha, por cabeçalho, por cabeçado e uma linha, e também
# e também cabeças e linhas, como uma tabela. 
def imprimir_atracao_linha(atracao):
    duracao_atracao = duracao(atracao['duracaoSegundos'])
    print(f"{atracao['atracao']:<35} | {atracao['precoAdulto']: ^15} | {atracao['precoCrianca']:^15} | {duracao_atracao:>10}") 

def atracao_header():
    print(f"{'Nome':^35} | {'Preço Adulto':^15} | {'Preço Criança':^15} | {'Duração':^10}") 
    print(f"{'-'*35} | {'-'*15} | {'-'*15} | {'-'*10}")
    
def imprimir_atracao_header(atracao):
    atracao_header()
    imprimir_atracao_linha(atracao)
        
def imprimir_atracoes(atracoes):
    atracao_header()
    for atracao in atracoes:
        imprimir_atracao_linha(atracao)


# Funções consulta do Engenheiro de manutenção
def atracoes_recorrencia():
    atracoes_recorrencias = {}
    vendas_atracoes_ids = []
    
    for item in vendas:
        vendas_atracoes_ids.append(item['atracao'])
    
    for item in vendas:
        atracoes_recorrencias[item['atracao']] = vendas_atracoes_ids.count(item['atracao'])
    
    return atracoes_recorrencias
    
#Função para saber qual a atração que dá mais lucro
def consultar_proximas_revisoes():
    proximas_revisoes = []
    atracoes_recorrencias = atracoes_recorrencia()

    for k, v in atracoes_recorrencias.items():
         rest = v % 50
         if rest > 0:
           atracao = find_atracao(k)  
           proximas_revisoes.append({
                "id": k,
                "nome_atracao": atracao['atracao'],
                "bilhete_restante": 50 - rest
            })
        
    return proximas_revisoes  

#Função principal - Menu do parque
def menu_principal():
    print("\n*** BEM-VINDO À CESAELAND! ***\n")
    
    while True:
        print("\n*** MENU CLIENTE ***\n")
        print("\n------------------------------------------\n")
        print("1. Consultar Atrações Disponíveis\n")
        print("2. Consultar Atração Favorita dos Adultos\n")
        print("3. Consultar Atração Favorita das Crianças\n")
        print("4. Login (funcionários)\n")            
        print("0. Sair\n")
        print("\n------------------------------------------\n")
       
        escolha = input("Escolha uma das opções: ")
        print("\n")
        
        if escolha == "1":
            consultar_atracoes_disponiveis()

        elif escolha == "2":
            atracao = atracao_mais_vendida('adulto')
            print(f"A atração favorita dos adultos é: {atracao['atracao']}.")
            # imprimir_atracao(atracao)
        
        elif escolha == "3":
            atracao = atracao_mais_vendida('crianca') 
            print(f"A atração favorita das crianças é: {atracao['atracao']}.")
            # imprimir_atracao(atracao)
                 
        elif escolha == "4":
            menu_login()

        elif escolha == "0":
            print("Programa encerrado!\n")
            break

        input("\nAperte qualquer tecla para continuar...")
    
# Menu principal do Parque
def menu_login():
    
    tipo_conta = login()

    if tipo_conta == "ADMIN":
        while True:
            print("\n*** MENU ADMINISTRADOR ***\n")
            print("\n--------------------------------------------------\n")
            print("1. Consultar o total de todas as vendas")
            print("2. Consultar o total de lucro")
            print("3. Consultar a atração mais procurada por adultos")
            print("4. Consultar a atração mais procurada por crianças")
            print("5. Consultar a atração mais lucrativa") 
            print("6. Consultar a atração menos lucrativa")                          
            print("7. Adicionar novo usuário")                          
            print("0. Sair")
            print("\n--------------------------------------------------\n")

            escolha = input("Escolha uma das opções: ")
            if escolha == "1":
                total = total_vendas()
                print(f"O valor total de vendas é: {total} €") 
            elif escolha == "2":
                total = float(total_vendas() - total_custos())
                print(f'O valor total do lucro é: { round(total, 2) } €')
                            
            elif escolha == "3":
                atracao = atracao_mais_vendida('adulto')
                print(f"A atração favorita dos Adultos é : {atracao['atracao']}.")
            
            elif escolha == "4":
                atracao = atracao_mais_vendida('crianca')
                print(f"A atração favorita das Crianças é : {atracao['atracao']}.")

            elif escolha == "5":
                atracao = atracao_lucro('max')
                imprimir_atracao_header(find_atracao(atracao["id"]))
                print("----------------------------------------------")
                print(f"Valor total do lucro é: {atracao['valor_total']} €") 
                 
            elif escolha == "6":
                atracao = atracao_lucro('min')
                imprimir_atracao_header(find_atracao(atracao["id"]))
                print("----------------------------------------------")
                print(f"Valor total do lucro é: {atracao['valor_total']} €")

            elif escolha == "7":
                adicionar_login()

            elif escolha == "0":
                print("Programa encerrado!")
                break
            
            input("\nAperte qualquer tecla para continuar...")        

    elif tipo_conta == "ENG":
        while True:
            print("\n*** MENU ENGENHEIRO DE MANUTENÇÃO ***")
            print("\n-------------------------------------------\n")
            print("1. Consultar Próximas Revisões")
            print("0. Sair")
            print("\n-------------------------------------------\n")

            escolha = input("Escolha uma opção: ")
            if escolha == "1":
                proximas_revisoes = consultar_proximas_revisoes()
                print(f"{'Id':^4} | {'Nome da Atração':^35} | {'Faltam':^10}") 
                print(f"{'-'*4} | {'-'*35} | {'-'*10}") 
                for atracao in proximas_revisoes:
                    print(f"{atracao['id']:^4} | {atracao['nome_atracao']:^35} | {atracao['bilhete_restante']:^10}") 
        
            elif escolha == "0":
                break
            


    
#consultar_proximas_revisoes()
menu_principal()