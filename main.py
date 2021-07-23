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
#	def _GetUnpermutedWord(self):
#		return tuple( (next(self.iterator),) )
#	def _GetPermutedWord(self):
#		word = next(self.iterator)
#		SwappedWord = SwapCase(word)
#		output = None
#		if word != SwappedWord:
#			output = tuple( (word, SwappedWord,) )
#		else:
#			output = tuple( (word,) )
#		return output
	def GetWord(self):
		output = None
		try:
			#output = self._GetWord()
			output = next(self.iterator)
		except (StopIteration, TypeError):
			self.iterator = None
		return output
	def reset(self):
		self._PrepareIterator()
	#def GetWords(self):
	#	output = []
	#	while True:
	#		w = self.GetWord()
	#		if w is None:
	#			break
	#		#output.extend(w)
	#		output.append(w)
	#	return output
	def AddWord(self, word):
		self.iterator = None
		self.words[word] = None
	def AddWords(self, words):
		for w in words:
			self.AddWord(w)
	#def EnablePermutations(self):
	#	self._GetWord = self._GetPermutedWord
	#def DisablePermutations(self):
	#	self._GetWord = self._GetUnpermutedWord
	def __init__(self):
		self.words = OrderedDict()
		self.iterator = None
		self._PrepareIterator()
		#self.DisablePermutations()

def MakeSpaceList():
	output = WordList()
	output.AddWord('')
	output.AddWord(' ')
	return output

def ParseCommandLine():
	"Function to create a command line argument parser, and return the args object from it."
	parser = argparse.ArgumentParser(description='Get command line arguments.')
	#parser.add_argument( '--permute-case', '-p', action='store_true', help='Permute upper case and lower case variants of each word.' )
	#parser.add_argument( '--space-words', '-s', action='store_true', help='Include permutations of words with spaces between them.' )
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
		#if args.permute_case:
		#	wl.EnablePermutations()
		WordLists.append(wl)
		#if args.space_words and FileName != args.input_files[-1]:
		#	WordLists.append( MakeSpaceList() )
	return WordLists

#def RenderWordLists(WordLists):
#	RenderedList = []
#	for wl in WordLists:
#		RenderedList.append( wl.GetWords() )
#	return RenderedList
#
#def PermuteWordList(RenderedList):
#	return permutations(RenderedList)

#def PrintWords(PermutedList):
#	for p in PermutedList:
#		print( ''.join(p) )

def PrintWords(WordLists, parts = []):
	for wl in WordLists:
		wl.reset()
		while True:
			w = wl.GetWord()
			if w is not None:
				parts.append(w)
				print( ''.join(parts) )
				PrintWords(WordLists[1:], parts)
				parts.pop()
			else:
				break

def main():
	args = ParseCommandLine()
	WordLists = GenerateWordLists(args)
	#RenderedList = RenderWordLists(WordLists)
	#PermutedList = PermuteWordList(RenderedList)
	#PrintWords(PermutedList)
	PrintWords(WordLists)

if __name__ == '__main__':
	main()
