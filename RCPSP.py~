# -*- coding: UTF-8 -*-
import string

offsetIni = 18
offsetFim = 32 + 4
numTasks = 32
tasks = []

#Limpa a linha e a coloca em lista
def clearLine(e):

	te = len(e) #captura o tamanho da linha
	i = 0
	v = []
	flag = 0
	word = ''
#Capturando os valores que sao de interesse para a execucao do algoritmo 
	while i < te:
		if e[i] == ' ':
			if flag == 1:
				#Inserindo os valores no vetor
				v.append(int(word))
				word = ''
				flag = 0
				i = i + 1
			else:		
				i = i + 1
		else:
			#Concatenando a palavra
			word = word + e[i]
			flag = 1
			i = i + 1
	#Adcionando o ultimo valor da linha no vetor		
	if word:		
		v.append(int(word))

	return v


#Carregando arquivo alimentar o algortimo
def load (nome_arq):
	
	arq = open(nome_arq, 'r')
	text = arq.read(); #lendo todo o arquivo para memoria
	lines = string.split(text, '\n') #Separando as linhas por \n
	nt = 0

	while nt < numTasks:
		#Selecionando parte dados do arquivo que sao de interesse para o algoritmo
		e1 = lines[offsetIni + nt]
		e2 = lines[offsetIni + offsetFim  + nt]

		#Limpa as linhas e salva em vetor os dados
		l1 = clearLine(e1)
		l2 = clearLine(e2)

		h1 = len(l1)
		h2 = len(l2)
			   #[NR da Tarefa, Sucessores, Recursos, Tempo de duracao da tarefa]
		tasks.append([l1[0], l1[3:h1], l2[2:h2], l2[2]]) 

		#print task

		nt = nt + 1

	geraPrecedentes()	

def ehPredecessor(t, pt):
	
	try:
		i = pt[1].index(t[0])
	except ValueError:	
		return -1
	else:
		return 1

#Cria a lista de predecessores
def geraPrecedentes():

	pred = []
	i = 0
	while i < numTasks:
		
		for t2 in tasks:
			if ehPredecessor(tasks[i], t2) == 1:
				pred.append(t2[0])
		tasks[i].append(pred)
		pred = []		
		i = i + 1



load('teste.sm')

for i in tasks:
	print i
