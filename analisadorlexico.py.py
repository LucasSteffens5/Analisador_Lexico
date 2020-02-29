# -*- coding: utf-8 -*-
import re as regex
import sys




#EXPRESSOES REGULARES DA LINGUAGUEM DEFINIDA PELO DIOGO
expressaoregular = [
    ('(if|else|begin|then|program|var|integer|const)',          'PALAVRARESERVADA'),
    ('(\.)',                                                    'FIM'),
    ('(>=|<=|==|!=|\=|>|<)',                                    'OPERADORRELACIONAL'),
    ('(:=)',                                                    'ATRIBUIÇÃO'),
    ('(\;|\,|\:|\(|\))',                                        'SIMBOLOESPECIAL'),
    ('([+-]?\d*\.\d+|\d+)',                                     'NUMEROREAL'),
    ('\d+',                                                     'NUMEROINTEIRO'),
    ('[\/\*]+[\w|W_\d\s\S]*[\*\/]+',                            'COMENTARIOEMBLOCO' ),
    ('[a-zA-Z_\d+]\w*',                                         'IDENTIFICADOR'),
    ('\+|\-|\*|\/|mod',                                         'OPERADORARITMÉTICO'),
]









class Token(): # Classe token, onde cada token tem um tipo, valor e posição
    def __init__(self, type, valor, posi):
        self.tipo = type
        self.valor = valor
        self.posi = posi

class Analisador():
    def __init__(self, expressaoregular, PularEspEmBranco = True):
        self.expressaoregular = [] # Vetor de expressaoregular (expreções regulares)
        self.PularEspEmBranco = PularEspEmBranco #Variavel auxuliar para retirar espaços em branco
        self.EspBrancos = regex.compile('\S')  # Compila para variavel a expresao regular de todos os tipos de espçamentos \s eh o parametro que indica as expressao regular q trata dos espaços

        for exp, tipo in expressaoregular: #Percorre as expreçoes nas expressaoregular
            self.expressaoregular.append((regex.compile(exp), tipo)) # Compila todas as expressoes regulares passadas nas expressaoregular

    def Entrada (self, buf): # Entrada dp buffer e iniciando da posição zero
        self.buffer = buf
        self.posi = 0

    def token(self):
        if self.posi >= len(self.buffer): #verifica se há mais dados no buffer a serem processados
            return None

        if self.PularEspEmBranco:
            aux = self.EspBrancos.search(self.buffer, self.posi) #Procura espaços para retirar
            if aux:
                self.posi = aux.start()
            else:
                return None

        for regex, tipo in self.expressaoregular: #Percorre e procura se casa com as expressaoregular
            casa = regex.match(self.buffer, self.posi)
            if casa: # Se casa com as expressaoregular variavel auxiliar recebe o token e retorna o token encontrado no buffer
                aux = Token(tipo, casa.group, self.posi)
                self.posi = casa.end()
                return aux



    def tokens(self):  # Funcao que cria a lista de tokens encontrados
        while 1:
            toker = self.token()
            if toker is None:
                break
            yield toker

lexer = Analisador(expressaoregular, PularEspEmBranco=True)
data = None

try:
    f = open(sys.argv[1], 'r+')  # abre o arquivo e le
    data = f.read()
    f.close()
except:
    if data is None:
        print('Erro ao abrir arquivo .txt')
        exit(1)

lexer.Entrada(data)

for toker in lexer.tokens():
    if toker.tipo!='COMENTARIOEMBLOCO':
        print("%s \t\t %s" %( toker.valor(0), toker.tipo))
