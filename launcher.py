import argparse
import re
import matplotlib.pyplot as plt
import asyncio

EXPR_PATTERN = re.compile(r'(\d+)d(\d+)')

async def main():
    parser = argparse.ArgumentParser(prog="Probability Grapher", description="Gives the likelyhood of each possible result for a set of dice")
    parser.add_argument("expr", nargs='+', help="An expression in the ndN where n is the number of dice and N is their max value. Several expressions can be specified, for many different dice types.")
    
    args = parser.parse_args()
    exprs = args.expr 
    allDiceTuples = []
    for expr in exprs:
        allDiceTuples.append(parseExpression(expr))
        
    values = createValueList(allDiceTuples)
    total = len(values)
    catalogue = catalogValues(values)
    for k in catalogue:
        catalogue[k] = 100*catalogue[k]/total
    asyncio.create_task(show(catalogue, exprs))
    catToPrint = catalogue.copy()
    for k in catToPrint:
        catToPrint[k] = str(round(catToPrint[k], 3)) + ' %'
    print(catToPrint)

def parseExpression(expr:str) -> tuple:
    matcher = EXPR_PATTERN.fullmatch(expr)
    if matcher == None:
        raise ValueError("'" + expr + "' is not a valid expression!" )
    dNum = int(matcher.group(1))
    dMax = int(matcher.group(2))
    return (dNum, dMax)

def addSeries(l1, l2) -> list:
    lout = list()
    for i in l1:
        for j in l2:
            lout.append(i+j)
    return lout

def createValueList(allDiceTuples:list) -> list:
    diceRanges = list()
    for dNum, dMax in allDiceTuples:
        r = range(1, dMax+1)
        for i in range(dNum):
            diceRanges.append(r)
    
    combinedValues = diceRanges.pop()
    for r in diceRanges:
        combinedValues = addSeries(combinedValues, r)
    
    return combinedValues

def catalogValues(values:list) -> map:
    catalogue = {}
    for v in values:
        num = catalogue.get(v)
        if num == None:
            num = 0
        
        catalogue[v] = num+1
    
    return catalogue

async def show(catalogue:dict, exprs:list) -> None:
    x = catalogue.keys()
    y = catalogue.values()
    plt.bar(x, y)
    plt.xlim(min(x), max(x))
    plt.xlabel('Result')
    plt.ylabel('Probability (%)')
    
    formatted = '+'.join(exprs)
    
    plt.title("Dice Value Probabilities for '" + formatted + "'")
    plt.show()

if __name__ == '__main__':
    asyncio.run(main())