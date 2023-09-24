import csv

filename = "shopping.csv"

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    ints = {0, 2, 4, 11, 12, 13, 14}
    floats = {1, 3, 5, 6, 7, 8, 9}
    months = {name: n 
        for n, name in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        )}

    evidence, labels = [], []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            ev = []
            for i in range(17):
                if i in ints:
                    e = int(row[i])
                elif i in floats:
                    e = float(row[i])
                elif i == 10:
                    e = months[row[i]]
                elif i == 15:
                    e = 1 if row[i] == "Returning_Visitor" else 0
                elif i == 16:
                    e = 1 if row[i] == "TRUE" else 0
                ev.append(e)
            evidence.append(ev)
            labels.append(1 if row[17] == "TRUE" else 0)

    return evidence, labels

evidence, labels = load_data(filename)
for i in range(10):
	print(evidence[-i], labels[-i])