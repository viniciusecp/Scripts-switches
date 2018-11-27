import os
import xlwt
import csv

from functools import partial
from tkinter import *

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

    # expandir portas Te
    listInterfaces2 = []
    for s in listInterfaces:
        if s.startswith('Te'):
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

    return listInterfaces3

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
                if txt[indiceInterface-1] == ' ':
                    while txt[indiceInterface] != '\n':
                        interfaces = interfaces + txt[indiceInterface]
                        indiceInterface = indiceInterface + 1
                if interfaces == '':
                    interfaces = '-'

                listInterfaces = quebraInterfaces(interfaces)
                dicionarioInterface[int(idVlan)] = listInterfaces

            except Exception as e:
                pass
        indice += 1

    return dicionarioInterface

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
    return cabecalhoInterface

def montarTabelaIpInterface(cabecalhoInterface, dicionarioFinal, dicionarioVlan, listVlansMostrar):
    # montar tabela de interfaces
    # utilizar o dicionario do cabeçalho para começo do dicionario tabela
    tabelaIpInterface = {}
    for ip, listInterfaces in cabecalhoInterface.items():
        dicionarioInterfaceVlan = {}
        for interface in listInterfaces:
            for ipAux, dicionarioVlanInterface in dicionarioFinal.items():
                if ip == ipAux:
                    listAux = []
                    for vlan, listInterfaceAux in dicionarioVlanInterface.items():
                        if interface in listInterfaceAux:
                            #monta lista com vlans de cada interface
                            listAux.append(vlan)
                    #verificar se esta no cabeçaho
                    listCabecalhoAux = []
                    for x in listVlansMostrar:
                        if x in listAux:
                            listCabecalhoAux.append(1)
                        else:
                            listCabecalhoAux.append(0)
            dicionarioInterfaceVlan[interface] = listCabecalhoAux
        tabelaIpInterface[ip] = dicionarioInterfaceVlan

    return tabelaIpInterface

def escreverPlanilha(fpath, tabelaIpInterface, dicionarioVlan, listVlansMostrar, listInterfacesMostrar):
    ############################################# GERAR PLANILHA VLAN

    style0 = xlwt.easyxf('font: name Arial, bold on;')
    #style1 = xlwt.easyxf('font: name Arial, color-index blue; pattern: pattern solid, fore_colour green;')
    style1 = xlwt.easyxf('font: name Arial;')
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
    style3 = xlwt.easyxf('font: name Arial, bold on; pattern: pattern solid, fore_colour blue;')

    # Definindo planilha
    wb = xlwt.Workbook()
    ws = wb.add_sheet('vlans')

    ############################################### Escrevendo tabela das INTERFACES FINAL
    linha = 0
    for ip, dicionarioInterfaceVlan in tabelaIpInterface.items():
        ws.write(linha, 0, ip, style0)
        for i in range(len(listVlansMostrar)):
            ws.write(linha+i+1, 0, listVlansMostrar[i], style3)

        coluna = 1
        for interface, listVlan in dicionarioInterfaceVlan.items():
            if interface in listInterfacesMostrar:
                ws.write(linha, coluna, interface, style0)
                linhaAux = linha
                for i in range(len(listVlan)):
                    linhaAux += 1
                    if listVlan[i] == 1:
                        ws.write(linhaAux, coluna, 'OK', style1)
                    else:
                        ws.write(linhaAux, coluna, '', style2)
                coluna += 1

        linha = linha + len(listVlansMostrar) + 1

    # Salvando
    wb.save(fpath+'vlans.xls')
    print('Planilha salva em:\n'+fpath+'vlans.xls')

def main(fpath, fpathCSV, listInterfacesMostrarAux):

    with open(fpathCSV, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            pass
    listVlansMostrar = []
    for l in row[0].split(","):
        listVlansMostrar.append(int(l))

    listInterfacesMostrarAux2 = listInterfacesMostrarAux.split(',')
    listInterfacesMostrar = []
    for i in listInterfacesMostrarAux2:
        listInterfacesMostrar.append(i.strip())

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

    cabecalhoInterface = montarCabecalhoInterfaces(dicionarioFinal)

    tabelaIpInterface = montarTabelaIpInterface(cabecalhoInterface, dicionarioFinal, dicionarioVlan, listVlansMostrar)

    escreverPlanilha(fpath, tabelaIpInterface, dicionarioVlan, listVlansMostrar, listInterfacesMostrar)
