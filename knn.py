import random
import math
from collections import Counter

#defini pessoa
class Pessoa:  
    def __init__(self, idade, sexo, salario, intencao_de_voto):
        self.idade = idade
        self.sexo = sexo
        self.salario = salario
        self.intencao_de_voto = intencao_de_voto
    #avalia expressao
    def __str__(self): 
        return f'idade: {self.idade}, sexo: {self.sexo}, salario: {round(self.salario,2)}, intencao_de_voto {self.intencao_de_voto}'
    #comparar voto
    def __eq__(self, other): 
        return self.intencao_de_voto == other.intencao_de_voto
    #hash
    def __hash__(self):
        return 1

def gera_base(n):
    lista = []
    for i in range(n):
        idade = random.randint(18, 35)
        sexo = random.choice(['M', 'F'])
        salario = 1200 + random.random() * 1300
        intencao_de_voto = random.choice(['Haddad', 'Bolsonaro'])
        p = Pessoa(idade, sexo, salario, intencao_de_voto)
        lista.append(p)
    return lista

def rotulo_de_maior_frequencia(pessoas):
    frequencias = Counter(pessoas)
    mais_frequentes = frequencias.most_common(1)
    return mais_frequentes[0][0]

def rotulo_de_maior_frequencia_sem_empate(pessoas):
    frequencias = Counter(pessoas)
    rotulo, frequencia = frequencias.most_common(1)[0]
    qtde_de_mais_frequentes = len(
        [count for count in frequencias.values() if count == frequencia])
    if qtde_de_mais_frequentes == 1:
        return rotulo
    return rotulo_de_maior_frequencia_sem_empate(pessoas[:-1])

def distancia(p1, p2):
    i = math.pow(p1.idade - p2.idade, 2)
    s = math.pow((1 if p1.sexo == 'M' else 0) -
                 (1 if p2.sexo == 'M' else 0), 2)
    sal = math.pow(p1.salario - p2.salario, 2)
    return math.sqrt(i + s + sal)

def knn(k, observacoes_rotuladas, nova_observacao):
    ordenados_por_distancia = sorted( observacoes_rotuladas, key=lambda obs: distancia(obs, nova_observacao))
    k_mais_proximos = ordenados_por_distancia[:k]
    resultado = rotulo_de_maior_frequencia_sem_empate(k_mais_proximos)
    return resultado.intencao_de_voto

#tarefa
def cross_validation_leave_one_out(pessoas, n):
    aux = 0
    for i in range(len(pessoas)):
        treinamento = []
        for j in range(len(pessoas)):
            if (i != j):
                treinamento.append(pessoas[j])
        if (knn(n, treinamento, pessoas[i]) == pessoas[i].intencao_de_voto):
            aux = aux + 1
    return aux / len(pessoas) * 100

def main():
    base = gera_base(100)
    for p in base:
        print(p)
    print(knn(5, base, Pessoa(19, 'F', 3500, None)))
    print(cross_validation_leave_one_out(base, 5))

main()