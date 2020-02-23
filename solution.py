import sys
import os

# Parsing input
fileName = sys.argv[1]
f = open(f'{fileName}.txt')

scoreFile = open("scores.txt", "r+")
score = int(scoreFile.readline())
scoreFile.seek(0, os.SEEK_SET)

nBooks, nLibraries, nDays = map(int, f.readline().split())
bookScores = list(map(int, f.readline().split()))
libraries = []
isBookShipped = [False] * nBooks

for i in range(nLibraries):
    nBooksinL, nSignup, shippingPerDay = map(int, f.readline().split())
    bookList = list(map(int, f.readline().split()))
    bookList.sort(key=lambda book: bookScores[book], reverse=True)
    sumOfBookScores = sum([bookScores[book] for book in bookList])
    avgOfBookScores = sumOfBookScores/nBooksinL
    booksOverAverageScore = [
        book for book in bookList if bookScores[book] >= avgOfBookScores]
    libraries.append(
        {
            "id": i,
            "nBooks": nBooksinL,
            "signupDays": nSignup,
            "shippingPerDay": shippingPerDay,
            "bookList": bookList,
            'sumOfBookScores': sumOfBookScores,
            'booksOverAverageScore': booksOverAverageScore,
            'uniqueBooks': []
        }
    )

# Previoulsy added the factors but that wasn't right approach
# since all the factors are of unit
""" 
libraries.sort(key=lambda x: x['signupDays'] + 1/x['sumOfBookScores'] +
               (1/x['nBooks'])+(0.0025/x['shippingPerDay'])+(0.00025/len(x['booksOverAverageScore'])))
 """

# Rewrote it as multiplicative factors based on a friend's idea
# Sorting libraries based on signupDays required and total value of books stored in the library
# Libraries with less signupDays and high value of books will be at first
libraries.sort(key=lambda x: x['signupDays'] / (x['sumOfBookScores']
                                                * x['shippingPerDay']))


# Keeping only unique books in the library
isBookAlreadyPresent = [False] * nBooks

for library in libraries:
    for book in library['bookList']:
        if not isBookAlreadyPresent[book]:
            isBookAlreadyPresent[book] = True
            library['uniqueBooks'].append(book)

    library['sumOfUniqueBookScores'] = sum([bookScores[book]
                                            for book in library['uniqueBooks']])
    if library['sumOfUniqueBookScores'] == 0:
        library['sumOfUniqueBookScores'] = 1

libraries.sort(key=lambda x: x['signupDays'] / (x['sumOfUniqueBookScores']
                                                * x['shippingPerDay']))

# output variables
signedUpLibraries = []
booksScannedFromLibraries = dict()
remainingDays = nDays

for i, library in enumerate(libraries):
    if remainingDays < library['signupDays']:
        break
    signedUpLibraries.append(library['id'])
    remainingDays -= library['signupDays']
    booksScannedFromLibraries[library['id']] = []
    for book in library['bookList'][:remainingDays * library['shippingPerDay']]:
        if not isBookShipped[book]:
            booksScannedFromLibraries[library['id']].append(book)
            isBookShipped[book] = True
    if len(booksScannedFromLibraries[library['id']]) == 0:
        signedUpLibraries.pop()
        remainingDays += library['signupDays']

# print(nBooks, nLibraries, nDays)
# print(bookScores)
# print(libraries)

outFile = open(f"{fileName}_out.txt", "w+")
outFile.truncate(0)
outFile.write(f"{len(signedUpLibraries)}\n")
for libraryID in signedUpLibraries:
    booksScanned = booksScannedFromLibraries[libraryID]
    outFile.write(f"{libraryID} {len(booksScanned)}\n")
    for i, book in enumerate(booksScanned):
        if i == len(booksScanned)-1:
            outFile.write(f"{book}\n")
        else:
            outFile.write(f"{book} ")
        score += bookScores[book]

scoreFile.write(str(score))
f.close()
outFile.close()
scoreFile.close()
