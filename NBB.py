from itertools import permutations, pairwise
from preGenDesigns import *

class NBB:

    def generate(numOfElements, numOfBlocks, isControl):
        blocks = []
        M = numOfElements - 1
        mType2 = numOfElements - 2
        # initiate an array of all elements
        elements = list((range(isControl, numOfElements+isControl)))
        

        # type 0 design
        if numOfElements in {4, 8, 9, 10, 12}:

            # as the method for type 0 design is not easily programmable, a dictonary
            # containing a complete list of designs is used

            readRange = numOfBlocks
            if numOfBlocks > len(preGenDesigns.preGenDict[numOfElements]):
                readRange = len(preGenDesigns.preGenDict[numOfElements])

            for i in range(readRange):
                processedBlock = [x+1 for x in preGenDesigns.preGenDict[numOfElements][i]]
                blocks.append(processedBlock)
        
        # type 1 design
        elif numOfElements in {3, 5, 7, 11, 13} and numOfBlocks == numOfElements:

            iterator1 = list((range(1, numOfElements+1)))
            iterator2 = [ -x for x in iterator1]
            iterator3 = [x for y in zip(iterator1, iterator2) for x in y]
            iterator = [0]
            iterator.extend(iterator3)

            # repeat for every block, in this case for every element
            for i in range(numOfElements):

                currentBlock = []
                #build the current block using an alternating list of positive and negative indeces
                for j in range(0, numOfElements-1):
                    #calculate the current index from the iterator modulo 2m
                    index = iterator[j]%M
                    # for every subsequent block created after the first, 1 is added to the iterator index
                    index = index + i
                    # if the given index is out of bounds, loop around to the correct index
                    if index >= numOfElements:
                        overflow = index-numOfElements
                        index = overflow
                    # add the treatment at the given index to the current block
                    currentBlock.append(elements[index])
                # add the current block to the final list of blocks
                blocks.append(currentBlock)

        # type 2 design is impossible to program due to the inclusion of the infinity element,
        # therefore its designs are split between other types

        # type 3 design
        elif numOfElements in {3, 5, 7, 11, 13} and numOfBlocks<numOfElements:

            # repeat for every requested block
            for i in range(1, numOfBlocks+1):
                currentBlock = []
                # the first element in a type 3 design is always the first treatment
                currentBlock.append(elements[0])

                # build the current block by setting every other element as j*i mod the number of treatments
                for j in range(1, numOfElements):
                    currentBlock.append(elements[j*i%numOfElements])
                # add the current block to the final list of blocks
                blocks.append(currentBlock)

        # no true method for the design of blocks with 6 elements is available, so fall back to the method used in the prototype
        elif numOfElements == 6:
            usedPairs = []
            for perm in permutations(elements):
                if len(blocks) == numOfBlocks:
                    break
                else:
                    pairsPerm = list(perm)
                    pairsPerm.append(pairsPerm[0])
                    pairs = list(pairwise(pairsPerm))
                if any(val in pairs for val in usedPairs) == False:
                    usedPairs.extend(pairs)
                    blocks.append(list(perm))

        return blocks

