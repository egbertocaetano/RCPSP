# -*- coding: UTF-8 -*-
import string
import random
import copy
import sys
import time
from numpy.random import choice, random_integers


offsetIni = 18
offsetFim = 32 + 4
offsetResource = 89
numTasks = 32
tasks = []
resourceAvailabilities	= {}
resourceUsage = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}

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
	l3 = clearLine(e3)
	
	resourceAvailabilities['R1'] = l3[0]
	resourceAvailabilities['R2'] = l3[1]
	resourceAvailabilities['R3'] = l3[2]
	resourceAvailabilities['R4'] = l3[3]
	
	generatePredecessors()	


def getActivity(num):
	
	for ativ in tasks:
		if ativ['NR'] == num:
			return ativ	

def isPredecessor(t, pt):
	
	try:
		i = pt['Sucessors'].index(t['NR'])
	except ValueError:	
		return -1
	else:
		return 1

def verifyAlreadyPredecessorsScheduled(predecessors, s):

	for p in predecessors:
		try:
			i = s.index(p) # Tenta recuperar a posição da atividade predecedente já escalonada
		except ValueError:
			return -1
		else:
			pass

	return 1

def orderActivities(Dg, asc):

	popElitist = sorted(Dg, key=lambda k: k['TimeDuration'])

	if asc:
		return popElitist
	else:
		popElitist.reverse()
		return popElitist
			
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
		#iterando sobre conjunto de predecedentes das atividades 
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

def getShortesElegibleActivitie(d):

	orderedElegiblesActivities = orderActivities(d,1)

	activ =  orderedElegiblesActivities.pop()

	for a in d:
		if activ['NR'] == a['NR']:
			try:
				i = d.index(a) # Tenta recuperar a posição da atividade predecedente já escalonada
			except ValueError:
				break
			else:
				pass

			act = d.pop(i)
			return act

	return -1		

#Atualizando quantidade de recursos no tempo inst
def updateResourceUsageTime(demand, resourceUsageTime, inst):

	for resource, amount in resourceUsageTime[inst].iteritems():
		if resource in demand:
			resourceUsageTime[inst][resource] = resourceUsageTime[inst][resource] + demand[resource] 

#Verificando quantidade de recursos disponiveis no tempo inst
def verifyResourceAvailabilities(demand,resourceUsageTime,inst):

	for resource, amount in resourceUsageTime[inst].iteritems():
		if resource in demand:
			if resourceUsageTime[inst][resource] + demand[resource] > resourceAvailabilities[resource]:
				return -1
	return 1
	
#Adicionando recursos em uso ao instante T
def allocatingActivityOnTimeLine(j,resourceUsageTime,inst): #Pensar em um outro nome para esse método
	
	isScheduled = False
	timeStart = inst
	reserveResourceInTime = []
	countTime = 0
	TimeEnd = 0
	limit = 0
	
	#print 'Time inst: ', inst, 'NR: ', j['NR'], 'TimeDuration: ', j['TimeDuration']
	
	#Procurano o instante o qual a atividade pode ser escalonada
	while isScheduled == False:

		limit = timeStart + j['TimeDuration']
		countTime = timeStart
		'''
		print 'timeStart', timeStart, 'countTime: ', countTime
		nome = raw_input("Debug: ")
		'''
		#Verificando se é possível alocar todos os recursos necessários para tempo de execução da atividade 
		for t in range(timeStart, limit):

			#Se não existe em resourceUsageTime, significa que desde instante em diante não há mais recursos alocados
			if t not in resourceUsageTime:
				#print 't: ', t
				resourceUsageTime[t] = {'R1' : 0, 'R2' : 0, 'R3' : 0, 'R4' : 0}
				updateResourceUsageTime(j, resourceUsageTime, t)
				countTime = countTime + 1
			#Verifica a disponibilidade dos recursos para esse determindo instante, 
			#caso tenha disponibilidade insere na lista de alocação de 	
			elif verifyResourceAvailabilities(j, resourceUsageTime,t) == 1:
				#print 't in verify: ', t
				reserveResourceInTime.append(t)
				countTime = countTime + 1
			else:
				break

		#print 'countTime: ', countTime, 'TimeEnd: ', timeStart + j['TimeDuration'] 		
		#Atualizando ResourceUsageTime		
		if countTime == limit:

			for t in reserveResourceInTime:
				updateResourceUsageTime(j, resourceUsageTime, t)					

			isScheduled	= True

			TimeEnd = timeStart + j['TimeDuration']
		else:
			countTime = 0
			timeStart = timeStart + 1	

	return TimeEnd	

#Serial Schedule Generation Scheme
def SGS():

	tp = [] #Conjunto de tarefas para serem processadas
	Dg = [] #Conjuto de atividades a serem escolhidas
	Sg = [] #Conjuto de atividades escolhida
	Rkt = [] #Quantidade de disponíveis recursos em tempo t
	F = []	#Tempo fim das atividades
	g = len(tasks) #Quantidade de ativdades do projeto
	et = [] #Ending Time (Tempo de términio)
	#etc = []
	resourceUsageTime = {} #Timeline de uso dos recursos
	individual = {} #Individuo gerado na execuç

	tp = copy.deepcopy(tasks)
	
	#Processando a primmeira atividade
	task = tp.pop(0)
	et.append({'NR':task['NR'], 'TimeEnd':0})
	#etc.append(0)
	Sg.append(task['NR'])
	F.append(1)
	resourceUsageTime[0] ={'R1' : 0, 'R2' : 0, 'R3' : 0, 'R4' : 0} #Inserindo uso dos recursos no instante 0

	i = 1
	while i < g:

		#função de seleção de atividades elegiveis
		selectElegibleActivities(Sg, Dg, tp)
		#Seleciona uma atividade de forma randomica
		j = getRandomElegibleActivitie(Dg)
		

		#Criar a função de consumo de resources	
		
		#Determinando o tempo de fim mais cedo da atividade j, ignorando a disponibilidade de recursos 
		#etc.append({'NR': j['NR'], 'TimeMaxPredecessor': getEarliestEndingPredecessor(j, et)})

		ES = getEarliestEndingPredecessor(j, et)

		#Adcionando o tempo fim da execução atividade j e atualização de recursos. 
		minJ = allocatingActivityOnTimeLine(j,resourceUsageTime,ES)

		
		et.append({'NR':j['NR'], 'TimeEnd': minJ}) 

		#Calculando o tempo final do conjunto
		F.append(et[-1])

		#Inserindo na lista de atividades já escalonadas	
		Sg.append(j['NR'])

		i = i + 1

	individual['Chromossome'] = Sg
	individual['Cost'] = F[-1]['TimeEnd']

	return individual

#Incío dos códigos dos operadores genéticos	
def generatePopulation(n):

	popu = []
	i = 0
	individual = {}

	while i < n:
		individual = SGS()
		if exsistsChromossome(individual, popu) == 1:#Verifica se o cromossomo já existe 
			#print 'Chromossome igual'
			individual = {}
		else:	
			popu.append(SGS())
			i = i + 1
	return popu

#Função para garantir que não existirá cromossomos iguais na população 
def exsistsChromossome(chromossome, population):
	
	for ind in population:
		if chromossome['Chromossome'] == ind['Chromossome']: 
			return 1

	return -1 		

#Ordena a população pelo custo menor tempo de execução
def classifyCandidates(pop):

	popElitist = sorted(pop, key=lambda k: k['Cost'])
	return popElitist

def selectsBestParents(pop, txSlection):

	poplength = len(pop)
	popCondidates = classifyCandidates(pop)
	selectQuantity = ((poplength*txSlection)/100)

	elit = popCondidates[0:selectQuantity]

	return elit

def crossover(ind1, ind2, candidates, qp):


	pointer = 0
	threshold = 0
	chromossome1 = []
	chromossome2 = []
	son1 = {}
	son2 = {}
	lenInd1 = len(ind1['Chromossome']) 
	lenInd2 = len(ind2['Chromossome'])
	listrandom = []
	offset = lenInd1/(qp+1)
	residual = lenInd1%(qp+1)
	set = 0

	#listrandom = range(0,lenInd1)
	#pointer =  random.choice(listrandom)

	if lenInd1 == lenInd2:
		#gerando filhos
		for i in range(1,qp+2):
			#print 'i: ', i, 'offset: ', offset, 'pointer: ' , pointer 
			threshold = (i*offset)

			if (i%2) == 1:
				chromossome1 += ind1['Chromossome'][pointer:threshold]
				chromossome2 += ind2['Chromossome'][pointer:threshold]
				pointer = threshold
			else:
				chromossome1 += ind2['Chromossome'][pointer:threshold]
				chromossome2 += ind1['Chromossome'][pointer:threshold]
				pointer = threshold
		
		if residual > 0:
			if ((threshold + residual)%2) == 1:
				chromossome1 += ind1['Chromossome'][pointer:threshold+residual]
				chromossome2 += ind2['Chromossome'][pointer:threshold+residual]
			else:
				chromossome1 += ind2['Chromossome'][pointer:threshold+residual]
				chromossome2 += ind1['Chromossome'][pointer:threshold+residual]
	else:
		print 'Pais com tamanho de gene diferente!'
		exit(1)

	son1['Chromossome'] = chromossome1	
	son2['Chromossome'] = chromossome2
	
	candidates.append(son1)
	candidates.append(son2)	

def crossoverWithBestParents(bestP, pop, candidates, qp):

	i = 1
	j = 0
	lengthBP = len(bestP)
	lengthPOP = len(pop)

	while i < lengthBP - 1:
		j = 1
		while j < lengthPOP - 2:
			crossover(bestP[i], pop[j], candidates, qp)
			j = j + 1
		i = i + 1	


def crossoverPopulation(pop, candidates, qp):

	i = 1
	j = 0
	length = len(pop)

	while i < length - 1:
		j = 1
		while j < length - 2:
			crossover(pop[i], pop[j], candidates, qp)
			j = j + 1
		i = i + 1	

def mutation(individual, candidates, probability):

	mutant =  copy.deepcopy(individual)
	length = len(mutant['Chromossome'])
	aux = 0
	candidate = {}

	i = 1 #Garante que não tentará fazer mutação na atividade 1, pois essa não importa porque ela é dummy
	while i < length - 2: ##Garante que não tentará fazer mutação na atividade 32, pois essa não importa porque ela é dummy
		if choice(2, p = [1-probability, probability]):
			#Altera essa parte para garantir que ele nao escolha o mesmo
			#chromossome.vect[x] = random_integers(1, Solution.solution_size)
			'''print 'Mutação:'
			print 'Gene1: ', mutant['Chromossome'][i] 
			print 'Gene2: ', mutant['Chromossome'][i+1] 
			print mutant['Chromossome']'''
			aux = mutant['Chromossome'][i+1]
			mutant['Chromossome'][i+1] = mutant['Chromossome'][i]			
			mutant['Chromossome'][i] = aux

			#print mutant['Chromossome']
		i = i + 1
	
	candidate['Chromossome'] = mutant['Chromossome'] 

	candidates.append(candidate)			

def mutaitonPopulation(pop, candidates, probability):

	for ind	in pop:
		mutation(ind, candidates, probability)

def hasRepeatedGene(chromossome):

	#print chromossome

	for gene in chromossome['Chromossome']:
		if chromossome['Chromossome'].count(gene) > 1:
			#print 'Nr: ' , gene, 'Chromossome: ', chromossome['Chromossome'].count(gene)
			return 1

	else:
		return -1		

def evaluationCandidate(candidate):

	if hasRepeatedGene(candidate) == 1:
		#print 'Genes repitidos!'
		return None

	#tp = [] #Conjunto de tarefas para serem processadas
	#Dg = [] #Conjuto de atividades a serem escolhidas
	Sg = [] #Conjuto de atividades escolhida
	Rkt = [] #Quantidade de disponíveis recursos em tempo t
	F = []	#Tempo fim das atividades
	g = len(tasks) #Quantidade de ativdades do projeto
	et = [] #Ending Time (Tempo de términio)
	#etc = []
	resourceUsageTime = {} #Timeline de uso dos recursos
	individual = {} #Individuo gerado na execução

	#tp = copy.deepcopy(tasks)
	
	
	#Processando a primmeira atividade
	#task = tp.pop(0)
	task = getActivity(candidate['Chromossome'][0])
	et.append({'NR':task['NR'], 'TimeEnd':0})
	#etc.append(0)
	Sg.append(task['NR'])
	F.append(1)
	resourceUsageTime[0] ={'R1' : 0, 'R2' : 0, 'R3' : 0, 'R4' : 0} #Inserindo uso dos recursos no instante 0


	i = 1
	while i < g:

		#função de seleção de atividades elegiveis
		#selectElegibleActivities(Sg, Dg, tp)
		#Seleciona uma atividade de forma randomica
		j = getActivity(candidate['Chromossome'][i])
		
		if verifyAlreadyPredecessorsScheduled(j['Predecessors'], Sg) == -1:
			#print 'Não foram todos escalonados'
			return None

		#Criar a função de consumo de resources	
		
		#Determinando o tempo de fim mais cedo da atividade j, ignorando a disponibilidade de recursos 
		#etc.append({'NR': j['NR'], 'TimeMaxPredecessor': getEarliestEndingPredecessor(j, et)})

		ES = getEarliestEndingPredecessor(j, et)

		#Adcionando o tempo fim da execução atividade j e atualização de recursos. 
		minJ = allocatingActivityOnTimeLine(j,resourceUsageTime,ES)

		
		et.append({'NR':j['NR'], 'TimeEnd': minJ}) 

		#Calculando o tempo final do conjunto
		F.append(et[-1])

		#Inserindo na lista de atividades já escalonadas	
		Sg.append(j['NR'])

		i = i + 1

	individual['Chromossome'] = Sg
	individual['Cost'] = F[-1]['TimeEnd']

	return individual

def selectsCandidates(candidatesFit, numberpopulation):
	
	classifiedList = classifyCandidates(candidatesFit)

	selectedCandidates = classifiedList[0:numberpopulation]

	return selectedCandidates


#def evaluationcandidates(newGeneration):


#############################################################################################################################################
#Início da execução do código

#Incio do algoritmo genético
numberpopulation = int(sys.argv[1])
numberpoints = int(sys.argv[2])
txSlection = int(sys.argv[3])
numberInteration = int(sys.argv[4])
instancia = sys.argv[5]
load(instancia)
txMutation = 0.1 #taxa de mutação de 1 porcento

Generations = []
numberGeneration = 0
population = generatePopulation(numberpopulation)
Generation = [{'NrGeneration' : numberGeneration, 'Population' : population}] 
bestParents = selectsBestParents(population, txSlection)
newGeneration = []
candidates = []
candidatesFit = []
counterIteration = 0
bestFitness = bestParents[0]['Cost'] 
bestFitnessNow = 0

#Inicio do algoritmo genético
timeBegin = time.clock()
while counterIteration <= numberInteration:

	numberGeneration = numberGeneration + 1
	bestParents = selectsBestParents(population, txSlection) # Recuperando os melhores individuos da população anterior
	population = generatePopulation(numberpopulation - len(bestParents)) # Gerando uma nova população
	population = population + bestParents # Unindo os melhores da população anterior com os da nova população

	#crossoverPopulation(population, candidates, numberpoints)

	crossoverWithBestParents(bestParents, population, candidates, numberpoints)
	mutaitonPopulation(population, candidates, txMutation)

	#Slecionando os candidatos em aptos
	for ind in candidates:
		candidate = evaluationCandidate(ind)
		if candidate == None:
			pass
		else:
			candidatesFit.append(candidate)

	newGeneration = selectsCandidates(candidatesFit, numberpopulation)

	bestFitnessNow = newGeneration[0]['Cost']

	#print counterIteration
	if bestFitnessNow >= bestFitness:
		counterIteration = counterIteration + 1
	else:
		print 'Geração: ', numberGeneration, ' Antigo: ' , bestFitness, ' Novo: ', bestFitnessNow
		bestFitness = bestFitnessNow
		counterIteration = 0

timeEnd = time.clock()

deltaTime = timeEnd - timeBegin

print instancia, ':' , bestFitness, ':' , deltaTime
