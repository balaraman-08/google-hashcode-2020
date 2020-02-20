import sys

# Parsing input
fileName = sys.argv[1]
f = open(f'{fileName}.txt')
nBooks, nLibraries, nDays = map(int, f.readline().split())
bookScores = list(map(int, f.readline().split()))
libraries = []
isBookShipped = [False] * nBooks

for i in range(nLibraries):
    nBooksinL, nSignup, shippingPerDay = map(int, f.readline().split())
    bookList = list(map(int, f.readline().split()))
    bookList.sort(key=lambda book: bookScores[book], reverse=True)
    libraries.append(
        {
            "id": i,
            "nBooks": nBooksinL,
            "signupDays": nSignup,
            "shippingPerDay": shippingPerDay,
            "bookList": bookList
        }
    )

libraries.sort(key=lambda x: x['signupDays'] +
               (1/x['nBooks'])+(1/x['shippingPerDay']))

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

# print(nBooks, nLibraries, nDays)
# print(bookScores)
# print(libraries)

outFile = open(f"{fileName}_out.txt", "w+")
outFile.write(f"{len(signedUpLibraries)}\n")
# print(len(signedUpLibraries))
score = 0
for libraryID in signedUpLibraries:
    booksScanned = booksScannedFromLibraries[libraryID]
    outFile.write(f"{libraryID} {len(booksScanned)}\n")
    # print(libraryID, len(booksScanned))
    for i,book in enumerate(booksScanned):
        if i == len(booksScanned)-1:
            outFile.write(f"{book}\n")
        else:
            outFile.write(f"{book} ")
    # print(*booksScanned)
f.close()
outFile.close()