# -*- coding: UTF-8 -*-
import string
import random


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
		tasks.append({'NR':l1[0], 'Predecessors':[], 'Sucessors':l1[3:h1],'R1': l2[3], 'R2': l2[4], 'R3': l2[5], 'R4':l2[6], 'TimeDuration':l2[2]}) 

		#print task

		nt = nt + 1

	#Capturando a quantidade de recursos	
	e3 = lines[offsetResource]

	resources = clearLine(e3)

	generatePredecessors()	

def isPredecessor(t, pt):
	
	try:
		i = pt['Sucessors'].index(t['NR'])
	except ValueError:	
		return -1
	else:
		return 1

#Recupera o último predecessor a terminar
def getEarliestEndingPredecessor(j, et):

	pft = {'NR': 0, 'TimeEnd': 0}

	for p in j['Predecessors']:
		for a in et:
			if p == a['NR']:
				if a['TimeEnd'] > pft['TimeEnd']:
					pft = a			
	return pft['TimeEnd']
#Cria a lista de predecessores
def generatePredecessors():

	pred = []
	i = 0
	while i < numTasks:
		
		for t2 in tasks:
			if isPredecessor(tasks[i], t2) == 1:
				pred.append(t2['NR'])
		tasks[i]['Predecessors'] = pred
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
		for p in t[count]['Predecessors']:
			try:
				i = s.index(p) # Tenta recuperar a posição da atividade predecedente já escalonada
			except ValueError:
				break
			else:
				cp = cp + 1
		#Verficando se a atividade tornou-se elegivel. Caso seja, adiciona ao conjunto d		
		if cp == len(t[count]['Predecessors']):
			d.append(t[count]) #Inserindo na lista de elegiveis
			listpop.append(t[count]) # Quardando referencia do objeto para excluir posteriormento

		count = count + 1
	
	#Removendo atividades da lista de atividades a serem processadas
	for pop in listpop:
		t.remove(pop)			

def getRandomElegibleActivitie(d):
	if not d:
		return -1
	else:	
		ra = random.choice(d)
		d.remove(ra)
		return ra
'''
#Adicionando recursos em uso ao instante T
def addResourceUsage(Rkj, Rkt, inst):

	for r in Rkt:
		if inst == r[0]:
			for 


def calculateRkt(j,Rkt,inst):
'''




#Serial Schedule Generation Scheme
def SGS():

	tp = tasks #Conjunto de tarefas para serem processadas
	Dg = [] #Conjuto de atividades a serem escolhidas
	Sg = [] #Conjuto de atividades escolhida
	Rkt = [] #Quantidade de disponíveis recursos em tempo t
	F = []	#Tempo fim das atividades
	g = len(tasks) #Quantidade de ativdades do projeto
	et = [] #Ending Time (Tempo de términio)
	etc = [] #
	#RU = 

	#Processando a primmeira atividade
	task = tp.pop(0)
	et.append({'NR':task['NR'], 'TimeEnd':0})
	etc.append(0)
	Sg.append(task['NR'])
	F.append(0)

	i = 1
	while i < g:

		#função de seleção de atividades elegiveis
		selectElegibleActivities(Sg, Dg, tp)
		#Seleciona uma atividade de forma randomica
		j = getRandomElegibleActivitie(Dg)
		
		#Criar a função de consumo de resources	
		

		#Determinando o tempo de fim mais cedo da atividade j, ignorando a disponibilidade de recursos 
		etc.append(getEarliestEndingPredecessor(j, et) + j['TimeDuration'])

		print etc

		#Adcionando a o tempo fim da atividade j. ISSO AINDA NÃO ESTÁ DO MODO CORRETO
		et.append({'NR':j['NR'], 'TimeEnd': etc[i]}) 

		#Calculando o tempo final do conjunto
		F.append(et[-1])

		#Inserindo na lista de atividades já escalonadas	
		Sg.append(j['NR'])

		i = i + 1




	print len(et)

	#print Sg	
	




#Início da execução do código

load('teste.sm')

'''
for i in tasks:
	print i
print "\n"
'''
SGS()

#for i in tasks:
#	print i