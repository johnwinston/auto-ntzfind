from subprocess import PIPE, Popen
import sys
import random
from random import randrange

outfile = open("PATH-TO-OUTFILE/outfile.txt", 'a')
cmd = "PATH-TO-NTZFIND/ntzfind"
sym = 'v'
depth = 'l200'
output = []
widthMin = 6
widthMax = 7
periodMin = 4
periodMax = 6
offsetMin = 1
offsetMax = 1

numbers = [1, 2, 3, 4, 5, 6, 7]
letters = [
            ['c', 'e'],
            ['c', 'e', 'k', 'a', 'i', 'n'],
            ['c', 'e', 'k', 'a', 'i', 'n', 'y', 'q', 'j', 'r'],
            ['c', 'e', 'k', 'a', 'i', 'n', 'y', 'q', 'j', 'r', 't', 'w', 'z'],
            ['c', 'e', 'k', 'a', 'i', 'n', 'y', 'q', 'j', 'r'],
            ['c', 'e', 'k', 'a', 'i', 'n'],
            ['c', 'e']
          ]
rule = ""

def genRule():
    global numbers, rule, letters
    rule = "b"
    numberOfNumbers = randrange(1, 8)
    numSamp = random.sample(numbers, numberOfNumbers)
    for i in range(numberOfNumbers):
        rule += str(numSamp[i])
        numberOfLetters = randrange(1, len(letters[numSamp[i]-1]))
        letSamp = random.sample(letters[numSamp[i]-1], numberOfLetters)
        for o in range(numberOfLetters):
            rule += str(letSamp[o])
    rule += "/s"

    numberOfNumbers = randrange(1, 8)
    numSamp = random.sample(numbers, numberOfNumbers)
    for i in range(numberOfNumbers):
        rule += str(numSamp[i])
        numberOfLetters = randrange(1, len(letters[numSamp[i]-1]))
        letSamp = random.sample(letters[numSamp[i]-1], numberOfLetters)
        for o in range(numberOfLetters):
            rule += str(letSamp[o])


def process(rule, width, period, offset, sym, depth):
    start = 0
    end = 0
    i = 0
    process = Popen(
                [cmd, rule, width, period, offset, sym, depth],
                shell=False,
                stdout=PIPE
                )
    while True:
        output.append(process.stdout.readline())
        if 'Starting search' in str(output[i]):
            start = i+2
        elif 'CPU time' in str(output[i]):
            start = i+1
        elif 'Length' in str(output[i]):
            end = i
        elif '0 spaceships' in str(output[i]):
            del output[:]
            break
        elif 'Spaceship found' in str(output[i]):
            outfile.write(rule + ' ' + width + ' ' + period + '\n')
            print(rule + ' ' + width + ' ' + period)
            for k in range(end - start):
                outfile.write(output[start+k].strip() + '\n')
                print(output[start+k].strip())
            del output[:]
            break
        i += 1


def main():
    global rule 
    while True:
        genRule()
        for i in range(widthMin, widthMax+1):
            for o in range(periodMin, periodMax+1):
                process(
                    rule,
                    'w'+str(i),
                    'p'+str(o),
                    'k'+str(1),
                    sym,
                    depth
                    )

def cleanup():
    outfile.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
