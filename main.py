from collections import OrderedDict
from itertools import permutations
import argparse

def SwapCase(word):
	output = word
	if output[0].isupper():
		output = ''.join( (output[0].lower(), output[1:]) )
	else:
		output = ''.join( (output[0].upper(), output[1:]) )
	return output

class WordList:
	def _PrepareIterator(self):
		if self.iterator is None:
			self.iterator = iter(self.words)
	def GetWord(self):
		output = None
		try:
			output = next(self.iterator)
		except (StopIteration, TypeError):
			self.iterator = None
		return output
	def reset(self):
		self._PrepareIterator()
	def AddWord(self, word):
		self.iterator = None
		self.words[word] = None
	def AddWords(self, words):
		for w in words:
			self.AddWord(w)
	def __init__(self):
		self.words = OrderedDict()
		self.iterator = None

def MakeSpaceList():
	output = WordList()
	output.AddWord('')
	output.AddWord(' ')
	return output

def ParseCommandLine():
	"Function to create a command line argument parser, and return the args object from it."
	parser = argparse.ArgumentParser(description='Get command line arguments.')
	parser.add_argument( 'input_files', nargs='+', help='List of dictionary files to be processed.' )
	return parser.parse_args()

def GenerateWordLists(args):
	WordLists = []
	for FileName in args.input_files:
		wl = WordList()
		handle = open(FileName, 'r')
		wl.AddWords( handle.read().splitlines() )
		wl.reset()
		handle.close()
		WordLists.append(wl)
	return WordLists

def PrintWords(WordLists, parts):
	if WordLists:
		wl = WordLists[0]
		wl.reset()
		while True:
			w = wl.GetWord()
			if w is not None:
				parts[len(parts) - len(WordLists)] = w
				print( ''.join(parts) )
				PrintWords(WordLists[1:], parts)
			else:
				for i in range( len(parts) - len(WordLists), len(parts) ):
					parts[i] = ''
				break

def main():
	args = ParseCommandLine()
	WordLists = GenerateWordLists(args)
	parts = ['' for wl in WordLists]
	PrintWords(WordLists, parts)

if __name__ == '__main__':
	main()
