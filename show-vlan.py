import os
import xlwt
#from functools import partial
#from tkinter import *

def formatarIOS(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("stdout")[2]
        text = text[5:]
        text = text[:len(text)-3]
        text = text.split("\nVLAN")[0]

        # deletar linha tracejada
        text = text[0:54] + text[134:]
    except Exception as e:
        pass

    file = open(fname, 'w')
    file.write(text)
    file.close()

    nomeArq = file.name
    nomeArq = nomeArq.split("/")
    nomeArq = nomeArq[len(nomeArq)-1]
    nomeArq = nomeArq.split("_")[0]

    return nomeArq, text

def formatarNexus(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("stdout")[2]
        text = text[5:]
        text = text[:len(text)-4]

        # deletar linha tracejada
        text = text[0:54] + text[134:]
    except Exception as e:
        pass

    file = open(fname, 'w')
    file.write(text)
    file.close()

    nomeArq = file.name
    nomeArq = nomeArq.split("/")
    nomeArq = nomeArq[len(nomeArq)-1]
    nomeArq = nomeArq.split("_")[0]

    return nomeArq, text

def formatarDell(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("stdout")[2]
        text = text[402:]
        text = text[:len(text)-4]

        #deletar 3 prfileimeiros caracteres iniciais
        caracteresDeletar = []
        for i in range(0,len(text)):
            if text[i] == '\n':
                caracteresDeletar.append(i+1)

        i = len(caracteresDeletar) - 1
        while i >= 0:
            indiceDeletar = caracteresDeletar[i]
            try:
                text = text[0:(indiceDeletar)] + text[indiceDeletar+4:]
            except Exception as e:
                pass
            i -= 1

        #deletar coluna Q
        caracteresDeletar = []
        caracteresDeletar.append(48)
        indice = 0
        while indice < len(text):
            if text[indice] == '\n':
                indiceInterno = indice + 49
                try:
                    caracteresDeletar.append(indiceInterno)
                except Exception as e:
                    pass
            indice += 1

        i = len(caracteresDeletar) - 1
        while i >= 0:
            indiceDeletar = caracteresDeletar[i]
            try:
                if text[indiceDeletar] == ' ' and text[indiceDeletar+2] == ' ':
                    text = text[0:(indiceDeletar)] + text[indiceDeletar+3:]
            except Exception as e:
                pass
            i -= 1
    except Exception as e:
        pass

    file = open(fname, 'w')
    file.write(text)
    file.close()

    nomeArq = file.name
    nomeArq = nomeArq.split("/")
    nomeArq = nomeArq[len(nomeArq)-1]
    nomeArq = nomeArq.split("_")[0]

    return nomeArq, text

def formatarQuebraLinha(path, txt):
    caracteresDeletar = []
    for i in range(0,len(txt)):
        try:
            if txt[i] == '\n' and txt[i+1] == ' ':
                caracteresDeletar.append(i)
        except Exception as e:
            pass

    i = len(caracteresDeletar) - 1
    while i >= 0:
        indiceDeletar = caracteresDeletar[i]
        try:
            txt = txt[0:(indiceDeletar)] + "," + txt[indiceDeletar+48:]
        except Exception as e:
            pass
        i -= 1

    file = open(path, 'w')
    file.write(txt)
    file.close()

    return txt

# esta função recebe a string do texto de arquivo e devolve uma lista com os ids de vlan
def listVlan(txt):
    #pegar ID VLAN
    list = []
    indice = 0
    while indice < len(txt):
        letra = txt[indice]
        if letra == '\n':
            indiceInterno = indice + 1
            idVlan = ''
            try:
                while txt[indiceInterno] != ' ':
                    idVlan = idVlan + txt[indiceInterno]
                    indiceInterno = indiceInterno + 1
                list.append(int(idVlan))
            except Exception as e:
                pass
        indice += 1
    return list

#esta função retorna um dicionario com key vlan e value uma lista de interfaces
#que é salvo em outro dicionario com key de ip e value o dicionario retornado no corpo do programa
def dictFinal(txt):
    dicionarioInterface = {}
    #pegar ID VLAN
    indice = 0
    while indice < len(txt):
        letra = txt[indice]
        if letra == '\n':
            indiceInterno = indice + 1
            idVlan = ''
            try:
                while txt[indiceInterno] != ' ':
                    idVlan = idVlan + txt[indiceInterno]
                    indiceInterno = indiceInterno + 1
                #pegar interface de cada VLAN
                indiceInterface = indice + 49
                interfaces = ''
                #listInterfaces = []
                if txt[indiceInterface-1] == ' ':
                    while txt[indiceInterface] != '\n':
                        interfaces = interfaces + txt[indiceInterface]
                        indiceInterface = indiceInterface + 1
                if interfaces == '':
                    interfaces = '-'

                listInterfaces = quebraInterfaces(interfaces)

                #dicionarioInterface[int(idVlan)] = listInterfaces2
                dicionarioInterface[int(idVlan)] = listInterfaces

            except Exception as e:
                pass
        indice += 1

    return dicionarioInterface

def quebraInterfaces(interfaces):
    listInterfaces = []
    posicaoVirgulas = []
    for i in range(len(interfaces)):
        if interfaces[i] == ',' and interfaces[i+1] == ' ':
            posicaoVirgulas.append(i)
    posicaoVirgulas.insert(0, 0)
    posicaoVirgulas.insert(len(posicaoVirgulas), len(interfaces))

    listAux = []
    for i in range(len(posicaoVirgulas)):
        if i == 0:
            pass
        elif i == 1:
            listAux.append(interfaces[posicaoVirgulas[i-1]:posicaoVirgulas[i]])
        else:
            listAux.append(interfaces[posicaoVirgulas[i-1]+1:posicaoVirgulas[i]])

    for x in listAux:
        listInterfaces.append(x.strip())

    #excluir os Po ou Eth
    '''listInterfaces2 = []
    for s in listInterfaces:
        print(s)
        if s.startswith('Eth'):
            pass
        else:
            listInterfaces2.append(s)'''

    # expandir portas Te
    listInterfaces2 = []
    for s in listInterfaces:
        if s.startswith('Te'):
            #expandir
            chave = s[:5]
            complemento = s[5:]
            complementoVirgula = complemento.split(',')

            listComplementos = []
            for n in complementoVirgula:
                if n.find('-') != -1:
                    #tem o caracter -
                    extremoInicial = int(n.split('-')[0])
                    extremoFinal = int(n.split('-')[1]) + 1
                    for x in range(extremoInicial, extremoFinal):
                        listInterfaces2.append(chave+str(x))
                else:
                    listInterfaces2.append(chave+n)
        else:
            listInterfaces2.append(s)

    listInterfaces3 = sorted(set(listInterfaces2))
    #listInterfaces3 = set(listInterfaces2)

    return listInterfaces3

def montarCabecalhoVLAN(dicionarioVlan):
    # montar cabeçalho de vlan
    cabecalhoVlan = []
    for key, value in dicionarioVlan.items():
        for x in value:
            if x in cabecalhoVlan:
                pass
            else:
                cabecalhoVlan.append(x)
    cabecalhoVlan.sort()
    #print("CABEÇALHO VLAN ###################################################")
    #print(cabecalhoVlan)
    return cabecalhoVlan

def montarTabelaVLAN(dicionarioVlan, cabecalhoVlan):
    # montar tabela de vlan
    #print("TABELA VLAN #######################################################")
    tabela = {}
    for key, value in dicionarioVlan.items():
        #print(key, value)
        list = []
        for x in cabecalhoVlan:
            if x in value:
                list.append(1)
            else:
                list.append(0)
        tabela[key] = list
    #for x, y in tabela.items():
        #print(x, y)
    return tabela

def montarCabecalhoInterfaces(dicionarioFinal):
    # montar cabeçalho de interfaces
    cabecalhoInterface = {}
    for ip, dicionarioVlanInterface in dicionarioFinal.items():
        cabecalhoAux = []
        for vlan, interface in dicionarioVlanInterface.items():
            for x in interface:
                if x in cabecalhoAux:
                    pass
                else:
                    if x != '-':
                        cabecalhoAux.append(x)
        cabecalhoInterface[ip] = cabecalhoAux
    #print("CABEÇALHO INTERFACES ###################################################")
    #print(cabecalhoInterface)
    return cabecalhoInterface

def montarTabelaInterfacesPorFiltro(dicionarioVlan, dicionarioFinal, cabecalhoVlan):
    # montar tabela de interfaces - NAO ESTA USANDO
    #print("TABELA INTERFACES #############################################################################")
    tabelaInterface = {}
    for key, value in dicionarioVlan.items():
        #key = ip; value = lista vlan de cada ip
        list = []
        for x in cabecalhoVlan:
            if x in value:
                #print(x)
                for ip, dicionarioVlanInterface in dicionarioFinal.items():
                    if ip == key:
                        for vlan, interface in dicionarioVlanInterface.items():
                            if vlan == x:
                                #print(interface)
                                if 'Fa0/3' in interface:
                                    list.append("OK")
                                else:
                                    list.append('-')
                                #list.append(interface)
            else:
                list.append('-')
        tabelaInterface[key] = list
    #for x, y in tabelaInterface.items():
        #print(x, y)
    return tabelaInterface

def montarTabelaIpInterface(cabecalhoInterface, dicionarioFinal, dicionarioVlan):
    # montar tabela de interfaces
    # utilizar o dicionario do cabeçalho para começo do dicionario tabela
    #print("TABELA INTERFACES TESTE #############################################################################")
    tabelaIpInterface = {}
    for ip, listInterfaces in cabecalhoInterface.items():
        #print("ip: "+ip+"------------------------------------------------------------------")
        dicionarioInterfaceVlan = {}
        for interface in listInterfaces:
            #print("interface: "+interface)
            for ipAux, dicionarioVlanInterface in dicionarioFinal.items():
                if ip == ipAux:
                    listAux = []
                    for vlan, listInterfaceAux in dicionarioVlanInterface.items():
                        #print("vlan:"+str(vlan)+" -> Lista interface: ")
                        #print(listInterfaceAux)
                        if interface in listInterfaceAux:
                            #monta lista com vlans de cada interface
                            listAux.append(vlan)
                    #verificar se esta no cabeçaho
                    listCabecalhoAux = []
                    # usar dicionarioVlan[ip] = [lista vlan]
                    for ip3, listVlans in dicionarioVlan.items():
                        if ip3 == ip:
                            for x in listVlans:
                                if x in listAux:
                                    listCabecalhoAux.append(1)
                                else:
                                    listCabecalhoAux.append(0)
                    '''for x in cabecalhoVlan:
                        if x in listAux:
                            listCabecalhoAux.append(1)
                        else:
                            listCabecalhoAux.append(0)'''
                    #print(cabecalhoVlan)
                    #print(listCabecalhoAux)
            dicionarioInterfaceVlan[interface] = listCabecalhoAux
        tabelaIpInterface[ip] = dicionarioInterfaceVlan

    '''print("CABEÇALHO VLAN ###################################################")
    print(cabecalhoVlan)
    print('TESTE tabelaIpInterface ################################################')
    for ip, dicionarioInterfaceVlan in tabelaIpInterface.items():
      print("IP: " + ip + "   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
      for interface, listVlan in dicionarioInterfaceVlan.items():
        print(interface, listVlan)'''

    return tabelaIpInterface

def escreverPlanilha(fpath, cabecalhoVlan, tabelaVlan, tabelaIpInterface, dicionarioVlan):
    ############################################# GERAR PLANILHA VLAN
    style0 = xlwt.easyxf('font: name Arial, bold on;')
    style1 = xlwt.easyxf('font: name Arial, color-index blue; pattern: pattern solid, fore_colour green;')
    style2 = xlwt.easyxf('font: name Arial, color-index blue;')

    # Definindo planilha
    wb = xlwt.Workbook()
    ws = wb.add_sheet('vlans')

    # Títulos das colunas
    titles = ['VLANs/IPs']
    titles.extend(cabecalhoVlan)

    # Escrevendo títulos na primeira coluna do arquivo
    for i in range(len(titles)):
        ws.write(i, 0, titles[i], style0)

    coluna = 1
    for x, y in tabelaVlan.items():
        # Obtendo a sequência do dicionário
        sequencia = y
        # Escrevendo o ip na 1ª linha da coluna i
        ws.write(0, coluna, x, style0)

        for j in range(len(sequencia)):
            if sequencia[j] == 1:
                ws.write(1+j, coluna, "OK", style1)
            else:
                ws.write(1+j, coluna, " ", style2)
        coluna += 1

    ############################################### Escrevendo tabela das INTERFACES FINAL
    '''
    for i in range(0, len(cabecalhoVlan)):
        ws.col(i+2).width = 1200
    '''
    # Títulos das colunas
    pularlinhas = len(titles) + 4
    '''ws.write(pularlinhas, 0, 'IPs', style0)
    ws.write(pularlinhas, 1, 'Interfaces', style0)'''

    vlanInicial = int(input('Vlan Inicial: '))
    vlanFinal = int(input('Vlan Final: '))
    #vlanInicial = int(edVlanInicial.get())
    #vlanFinal = int(edVlanFinal.get())

    listInterfacesMostrarAux = input('Lista de interfaces separadas por virgulas: ').split(',')
    #listInterfacesMostrarAux = edInterfaces.get().split(',')
    listInterfacesMostrar = []
    for i in listInterfacesMostrarAux:
        listInterfacesMostrar.append(i.strip())

    #listInterfacesMostrar = ['Po46', 'Eth1/2']

    linha = pularlinhas+1
    for ip, dicionarioInterfaceVlan in tabelaIpInterface.items():
        ws.write(linha, 0, ip, style0)
        ws.write(linha, 1, 'VLAN/Ports', style0)

        listVlans = dicionarioVlan[ip]

        #buscar vlans inicial e final
        posicaoVlanInicial = 0
        posicaoVlanFinal = len(listVlans) - 1
        indice = 0
        for v in listVlans:
            if v == vlanInicial or v > vlanInicial:
                posicaoVlanInicial = indice
                break
            indice += 1
        indice = 0
        for v in listVlans:
            if v == vlanFinal:
                posicaoVlanFinal = indice
                break
            elif v > vlanFinal:
                posicaoVlanFinal = indice-1
                break
            indice += 1

        print(posicaoVlanInicial)
        print(posicaoVlanFinal)

        if posicaoVlanInicial > posicaoVlanFinal:
            print("Não há vlans nesse intervalo!")
        else:
            '''for i in range(len(listVlans)):
                ws.write(linha+i+1, 1, listVlans[i], style0)'''
            '''for i in range(len(cabecalhoVlan)):
                ws.write(linha+i+1, 1, cabecalhoVlan[i], style0)'''
            quantidadePulaLinha = 0
            for x in range(posicaoVlanInicial, posicaoVlanFinal+1):
                ws.write(linha+quantidadePulaLinha+1, 1, listVlans[x], style0)
                quantidadePulaLinha += 1
            coluna = 2
            for interface, listVlan in dicionarioInterfaceVlan.items():
                if interface in listInterfacesMostrar:
                    ws.write(linha, coluna, interface, style0)
                    linhaAux = linha
                    '''for i in range(len(listVlan)):
                        linhaAux += 1
                        if listVlan[i] == 1:
                            ws.write(linhaAux, coluna, 'OK', style1)'''
                    quantidadePulaLinha = 0
                    for x in range(posicaoVlanInicial, posicaoVlanFinal+1):
                        linhaAux += 1
                        if listVlan[x] == 1:
                            ws.write(linhaAux, coluna, 'OK', style1)
                    coluna += 1

        linha = linha + (posicaoVlanFinal - posicaoVlanInicial) + 3

    # Salvando
    wb.save(fpath+'vlans.xls')
    #lb4["text"] = 'Planilha salva em:\n'+fpath+'vlans.xls'
    print('Planilha salva em:\n'+fpath+'vlans.xls')

def main():

    print("Processando...")
    #fpath = '/home/vinicius/Desktop/'
    fpath = input('Caminho da pasta: ')
    #fpath = edPath.get()

    caminhos = [os.path.join(fpath, nome) for nome in os.listdir(fpath)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    ios = [arq for arq in arquivos if arq.lower().endswith("ios.txt")]
    nexus = [arq for arq in arquivos if arq.lower().endswith("nexus.txt")]
    dell = [arq for arq in arquivos if arq.lower().endswith("dell.txt")]

    dicionarioVlan = {}
    dicionarioFinal = {}

    for path in ios:
        nomeArqIOS, textIOS = formatarIOS(path)
        textIOS = formatarQuebraLinha(path, textIOS)

        dicionarioVlan[nomeArqIOS] = listVlan(textIOS)
        dicionarioFinal[nomeArqIOS] = dictFinal(textIOS)

    for path in nexus:
        nomeArqNEXUS, textNEXUS = formatarNexus(path)
        textNEXUS = formatarQuebraLinha(path, textNEXUS)

        dicionarioVlan[nomeArqNEXUS] = listVlan(textNEXUS)
        dicionarioFinal[nomeArqNEXUS] = dictFinal(textNEXUS)

    for path in dell:
        nomeArqDELL, textDELL = formatarDell(path)
        textDELL = formatarQuebraLinha(path, textDELL)

        dicionarioVlan[nomeArqDELL] = listVlan(textDELL)
        dicionarioFinal[nomeArqDELL] = dictFinal(textDELL)

    cabecalhoVlan = montarCabecalhoVLAN(dicionarioVlan)

    tabelaVlan = montarTabelaVLAN(dicionarioVlan, cabecalhoVlan)

    cabecalhoInterface = montarCabecalhoInterfaces(dicionarioFinal)

    #não esta sendo usado
    tabelaInterfacePorFiltro = montarTabelaInterfacesPorFiltro(dicionarioVlan, dicionarioFinal, cabecalhoVlan)

    tabelaIpInterface = montarTabelaIpInterface(cabecalhoInterface, dicionarioFinal, dicionarioVlan)

    escreverPlanilha(fpath, cabecalhoVlan, tabelaVlan, tabelaIpInterface, dicionarioVlan)

############################################# INTERFACE GRAFICA
main()
'''
janela = Tk()
janela.title("Show VLAN")

lb1 = Label(janela, text="Digite o caminho da pasta:")
lb1.place(x=100, y=25)

edPath = Entry(janela, )
edPath.place(x=100, y=55)

lb2 = Label(janela, text="Intervalo de vlans:")
lb2.place(x=100, y=85)

edVlanInicial = Entry(janela, width=5)
edVlanInicial.place(x=100, y=115)

lb3 = Label(janela, text="a")
lb3.place(x=160, y=115)

edVlanFinal = Entry(janela, width=5)
edVlanFinal.place(x=185, y=115)

lb5 = Label(janela, text="Interfaces separadas por virgulas:")
lb5.place(x=100, y=145)

edInterfaces = Entry(janela, )
edInterfaces.place(x=100, y=175)

btnOK = Button(janela, width=20, text="OK", command=main)
btnOK.place(x=100, y=210)

lb4 = Label(janela, text="")
lb4.place(x=100, y=260)

#LARGURAxALTURA+DISTANCIAesquerda+DISTACIAtopo
#400x300+200+100
janela.geometry("360x330+800+100")

janela.mainloop()
'''
