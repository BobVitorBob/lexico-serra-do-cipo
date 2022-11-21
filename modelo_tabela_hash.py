import math
import time
import random
import pandas as pd
import sys
from os import system, name

def clear():
    if name == 'nt': system('cls')
    else: system('clear')

def is_prime(number):
	"""
	Diz se um número é primo
	"""
	# 1 e 2 falham no loop mas são primos
	if (number == 1) or (number == 2): return True
	# numeros de 2 até number/2, somando de 2 em 2
	# Se não tiver nenhum divisor, é primo
	if (number % 2 == 0): return False
	for i in range(3, math.floor(number/2)+1, 2):
		if (number % i) == 0: return False
	return True

def next_prime(number):
	"""
	Acha o próximo primo.
	"""
	# Se for primo, retorna o próprio número
	if is_prime(number): return number
	# Se não, chama a função de novo pro próximo candidato
	return next_prime(number + 1 if (number % 2) == 0 else number + 2)

class TabelaHash:
	# Construtor
	def __init__(self, tamanho_vocabulario: int):
		# Calculando tamanho do fator de carga
		load_factor_size = math.ceil(tamanho_vocabulario / 0.75)

		self.tabela_size = next_prime(load_factor_size)
		self.tabela_hash = [[] for i in range(self.tabela_size)]

	# Função de hash AHO
	def __funcao_AHO(self, chave: str):
		hash = 0
		# Valor de alfa, pode ser qualquer número inteiro > 1
		alfa = 10
		for indice, char in enumerate(chave):
			# Faz a múltiplicação da hash antiga pelo alfa, e depois soma o valor do char
			hash += (alfa * hash) + ord(char)

		return hash % self.tabela_size

	# Função de inserção na hash
	def insert(self, chave: str, valor, print_time=False):
		if print_time: elapsed = time.time()
		
		lista = self.tabela_hash[self.__funcao_AHO(chave)]

		for item in lista:
		# Se o item já existe, tira ele da posição
			if item['chave'] == chave:
				lista.remove(item)
				break
		lista.append({'chave': chave, 'valor': valor})
		if print_time: print('Tempo de inserção: ', time.time() - elapsed)
	# Função de remoção da hash
	def remove(self, chave, print_time=False):
		if print_time: elapsed = time.time() 
		lista = self.tabela_hash[self.__funcao_AHO(chave)]

		for item in lista:
			if item['chave'] == chave:
				lista.remove(item)
				break
		if print_time: print('Tempo de deleção: ', time.time() - elapsed)
	# Função de recuperação da hash. Assume que não possa ter mais de uma chave repetida
	def get(self, chave, print_time=False):
		if print_time: elapsed = time.time()
		lista = self.tabela_hash[self.__funcao_AHO(chave)]
		
		for item in lista:
			if item['chave'] == chave:
				if print_time: print('Tempo de recuperação: ', time.time() - elapsed)
				return item['valor']
	# Função de stringify da tabela hash. Retorna uma string pra quando print(tabela) é chamado
	def __str__(self):
		string = 'Tamanho total da tabela: ' + str(self.tabela_size) + '\n'
		for i in range(self.tabela_size):
			string_parcial = 'Posição ' + str(i) + '({} itens)'.format(len(self.tabela_hash[i])) + ': \n\n'
			for j in range(len(self.tabela_hash[i])):
				string_parcial += '{}: {}\n'.format(str(self.tabela_hash[i][j]['chave']), str(self.tabela_hash[i][j]['valor']))
				if j != len(self.tabela_hash[i]): string_parcial += '\n'

			string += string_parcial + '\n\n'
		return string

# Lendo o csv pra pegar o dataframe
df = pd.read_csv('Cafe.csv')

# Criando a tabela

vocab_size = len(df)
tabela = TabelaHash(vocab_size)

# Inserindo os itens

for index, row in df.iterrows():
    tabela.insert(row['palavra'].lower(), {
        'palavra': row['palavra'],
		'dicionarizado': row['dicionarizado'],
		'categoria_gramatical': row['categoria_gramatical'],
		'idioma_origem': row['idioma_origem'],
		'definicao': row['definicao'],
		'frase_de_abonacao': row['frase_de_abonacao'],
    })

# Loop da interface

while(True):
	print('Tabela Hash!')
	print('Léxico do Café\n')
	print('Escolha uma opção: \n')
	print('1. Inserir item')
	print('2. Recuperar item')
	print('3. Deletar item')
	print('4: Mostrar Tabela')
	print('5: Teste de performance')
	print('6: Sair')
	escolha_usuario = input()

	clear()

	if (escolha_usuario == '1') or (escolha_usuario.lower() == 'inserir') or (escolha_usuario.lower() == 'inserir item'):
		print('Digite a chave do item que será inserido')
		chave_item = input()
		clear()
		item = {}
		while True:
			print('Digite a chave e o valor da chave no dicionário, ou digite \'q!\' finalizar')
			chave = input()
			if chave == 'q!': break
			valor = input()
			if valor == 'q!': break
			item[chave.lower()] = valor
			clear()
		tabela.insert(chave_item.lower(), item)
		print('Item {} inserido na tabela'.format(item))
		print('Aperte Enter para continuar')
		input()

	elif (escolha_usuario == '2') or (escolha_usuario.lower() == 'recuperar') or (escolha_usuario.lower() == 'recuperar item'):
		print('Digite a chave do item que será recuperado')
		chave_item = input()
		clear()
		item = tabela.get(chave_item.lower())
		if item is None: print('Item não encontrado!')
		else: print('Item recuperado!', item, '')
		print('Aperte Enter para continuar')
		input()

	elif (escolha_usuario == '3') or (escolha_usuario.lower() == 'deletar') or (escolha_usuario.lower() == 'deletar item'):
		print('Digite a chave do item que será deletado')
		chave_item = input()
		tabela.remove(chave_item.lower())
		clear()
		print('Item removido!')
		print('Aperte Enter para continuar')
		input()

	elif (escolha_usuario == '4') or (escolha_usuario.lower() == 'mostrar') or (escolha_usuario.lower() == 'mostrar tabela'):
		print(tabela)
		print('Aperte Enter para continuar')
		input()

	elif (escolha_usuario == '5') or (escolha_usuario.lower() == 'teste') or (escolha_usuario.lower() == 'teste de velocidade'):
		chaves = [(str(x) + str(x) + str(x)).zfill(20) for x in range(1000000)]
		print('Mudando tamanho da tabela')
		comeco = time.time()
		vocab_size = 1000000
		tabela_teste = TabelaHash(vocab_size)
		fim = time.time()
		print('Tempo de criacao:', fim - comeco)
		print('Tamanho da tabela:', tabela_teste.tabela_size)
		print('Inserindo 1000000 itens com chaves de 20 caracteres')
		comeco = time.time()
		for chave in chaves:
			tabela_teste.insert(chave.lower(), {'valor': chave, 'chave': chave})
		fim = time.time()
		print('Tempo de insercao:', fim - comeco)
		print('Média do tempo de insercao:', (fim - comeco)/1000000)
		print('Recuperando 1000000 itens')
		comeco = time.time()
		for chave in chaves:
			tabela_teste.get(chave.lower())
		fim = time.time()
		print('Tempo de recuperação:', fim - comeco)
		print('Média do tempo de recuperação:', (fim - comeco)/1000000)
		print('Deletando 1000000 itens')
		comeco = time.time()
		for chave in chaves:
			tabela_teste.remove(chave.lower())
		fim = time.time()
		print('Tempo de deleção:', fim - comeco)
		print('Média do tempo de deleção:', (fim - comeco)/1000000)
		print('Aperte Enter para continuar')
		input()

	elif (escolha_usuario == '6') or (escolha_usuario.lower() == 'sair')):
		sys.exit()
	else:
		print('Digite uma opção válida!')
		time.sleep(3)

	clear()
