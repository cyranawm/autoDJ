#for a 10 songs mix, this returns the list of the names of the songs involved in the obvious mix

def obvious_full(dir):
	file = open(dir+"readme.txt","r")
	data = file.read()
	words = data.split()
	names = [words[0], words[3]]
	return names

def obvious_genre(dir):
	file = open(dir+"readme.txt","r")
	data = file.read()
	words = data.split()
	return words

def obvious_partial(dir):
	file = open(dir+"readme.txt","r")
	data = file.readlines()
	words = []
	for line in data:
		words.append(line.split())
	names = [l[0] for l in words]
	return names



