import os

def formatarIOS(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("Current configuration")[2]
        text = "Current configuration" + text
        text = text[:len(text)-3]
    except Exception as e:
        raise

    file = open(fname, 'w')
    file.write(text)
    file.close()

def formatarNexus(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("!Command: show running-config")[2]
        text = "!Command: show running-config" + text
        text = text[:len(text)-3]
    except Exception as e:
        raise

    file = open(fname, 'w')
    file.write(text)
    file.close()

def formatarDell(path):
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    try:
        text = text.replace('\\n', '\n' )
        text = text.replace('\\t', '\t' )
        text = text.split("Current Configuration")[2]
        text = "Current Configuration" + text
        text = text[:len(text)-3]
    except Exception as e:
        raise

    file = open(fname, 'w')
    file.write(text)
    file.close()

main():
    #fpath = '/home/vinicius/Desktop/'
    fpath = input('Caminho da pasta: ')

    caminhos = [os.path.join(fpath, nome) for nome in os.listdir(fpath)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    ios = [arq for arq in arquivos if arq.lower().endswith("ios.txt")]
    nexus = [arq for arq in arquivos if arq.lower().endswith("nexus.txt")]
    dell = [arq for arq in arquivos if arq.lower().endswith("dell.txt")]

    for path in ios:
        formatarIOS(path)
    for path in nexus:
        formatarNexus(path)
    for path in dell:
        formatarDell(path)

main()
