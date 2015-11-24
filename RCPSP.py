import string

offsetIni = 18
offsetFim = 32 + 4
numTasks = 32

#Limpa a linha e a coloca em lista
def clearLine(e):

	te = len(e)
	i = 0
	v = []
	flag = 0
	word = ''

	while i < te:
		if e[i] == ' ':
			if flag == 1:
				v.append(int(word))
				word = ''
				flag = 0
				i = i + 1
			else:		
				i = i + 1
		else:
			word = word + e[i]
			flag = 1
			i = i + 1

	if word:		
		v.append(int(word))

	return v



def load (nome_arq):
	
	arq = open(nome_arq, 'r')
	text = arq.read();
	lines = string.split(text, '\n')
	nt = 0
	while nt < numTasks:
		e1 = lines[offsetIni + nt]
		e2 = lines[offsetIni + offsetFim  + nt]

		l1 = clearLine(e1)
		l2 = clearLine(e2)

		h1 = len(l1)
		h2 = len(l2)

		task = [l1[0], l1[2:h1], l2[2:h2], l2[2]]

		print task

		nt = nt + 1


load('teste.sm')