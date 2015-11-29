# -*- coding: UTF-8 -*-
import string

offsetIni = 18
offsetFim = 32 + 4
offsetResource = 89
numTasks = 32
tasks = []
resources = []

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

	#Capturando a quantidade de recursos	
	e3 = lines[offsetResource]

	resources = clearLine(e3)

	generatePredecessors()	

def isPredecessor(t, pt):
	
	try:
		i = pt[1].index(t[0])
	except ValueError:	
		return -1
	else:
		return 1

#Cria a lista de predecessores
def generatePredecessors():

	pred = []
	i = 0
	while i < numTasks:
		
		for t2 in tasks:
			if isPredecessor(tasks[i], t2) == 1:
				pred.append(t2[0])
		tasks[i].append(pred)
		pred = []		
		i = i + 1


def selectElegibleActivities(s, d, t):

	length = len(t) 
	count = 0
	listpop = []

	#iterando sobre conjunto de atividades a serem processadas
	while count < length: #for a in t:
		cp = 0
		#iterando sobre conjunto de predecedentes da atividades 
		for p in t[count][4]:
			try:
				i = s.index(p) # Tenta recuperar a posição da atividade predecedente já escalonada
			except ValueError:
				break
			else:
				cp = cp + 1
		#Verficando se a atividade tornou-se elegivel. Caso seja, adiciona ao conjunto d		
		if cp == len(t[count][4]):
			d.append(t[count]) #Inserindo na lista de elegiveis
			listpop.append(t[count]) # Quardando referencia do objeto para excluir posteriormento

		count = count + 1
	
	#Removendo atividades da lista de atividades a serem processadas
	for pop in listpop:
		try:
			i = t.index(pop)
			t.pop(i)			
		except ValueError:
			print "Erro: Ocorreu um erro ao tentar excluir um elemento da lista de atividades a serem processadas"	
		
	


	#return d	

#Serial Schedule Generation Scheme
def SGS():

	tp = tasks #Conjunto de tarefas para serem processadas
	Dg = [] #Conjuto de atividades a serem escolhidas
	Sg = [] #Conjuto de atividades escolhida
	Rk = [] #Conjuto de recursos
	F = 0	#Custo da solução gerada
	g = len(tasks) #Quantidade de ativdades do projeto
	st = [g] #Starting time (Tempo de início da atividade)
	et = [g] #Ending Time (Tempo de términio) 
	RU = [len(resources)]

	#Processando a primmeira atividade
	task = tp.pop(0)
	st[0] = et = 0
	Sg.append(task[0])

	#ISSO ESTÁ ERRADO! Inserindo sucessores para o vetor de atividades a serem escolhidas
	#Dg = task[1]

	selectElegibleActivities(Sg, Dg, tp)
	print Dg
	print "\n"
	for i in tp:
		print i

	'''
	i = 1
	while i < g:

		selectElegibleActivities(Sg, Dg, tp)
		print Dg
		i = i + 1
		#Fazer uma função de seleção de atividades elegiveis
	'''	


	










#Início da execução do código



load('teste.sm')

for i in tasks:
	print i
print "\n"
SGS()

#for i in tasks:
#	print i