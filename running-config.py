import os

#fpath = '/home/vinicius/Desktop/'
fpath = input('Caminho da pasta: ')

caminhos = [os.path.join(fpath, nome) for nome in os.listdir(fpath)]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
txt = [arq for arq in arquivos if arq.lower().endswith(".txt")]

for path in txt:
    fname = path
    file = open(fname, 'r')
    text = file.read()
    file.close()

    text = text.replace('\\n', '\n' )
    text = text.replace('\\t', '\t' )
    text = text.split("Current configuration")[2]
    text = "Current configuration" + text
    text = text[:len(text)-3]

    file = open(fname, 'w')
    file.write(text)
    file.close()
