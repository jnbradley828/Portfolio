def arithmetic_arranger(problems, solution=False):
    ###Split operands/operator into list and program errors.

    # Reject if there are more than 5 items.
    if len(problems) > 5:
        return ('Error: Too many problems.')

    # split into operands and operator
    splitProbs = list()
    for problem in problems:
        splitProb = problem.split()
        splitProbs.append(splitProb)
    # print(splitProbs)

    # Reject if something besides numbers are given.
    for prob in splitProbs:
        try:
            int(prob[0]) and int(prob[2])
        except:
            return ('Error: Numbers must only contain digits.')

    # Reject if number is longer than 4 digits.
    for prob in splitProbs:
        if len(prob[0]) > 4 or len(prob[2]) > 4:
            return ('Error: Numbers cannot be more than four digits.')

    # Reject if operator is not + or -
    for prob in splitProbs:
        if prob[1] != '-' and prob[1] != '+':
            return ('Error: Operator must be \'+\' or \'-\'.')

    ###Add spaces and split into lines

    # add spaces before shorter number until equal length.
    for prob in splitProbs:
        while len(prob[0]) < len(prob[2]):
            prob[0] = ' ' + prob[0]
        while len(prob[2]) < len(prob[0]):
            prob[2] = ' ' + prob[2]
    # print(splitProbs)

    # start creating the arranged problems string line by line
    line1 = '  '
    for prob in splitProbs:
        if line1 == '  ':
            line1 += prob[0]
        else:
            line1 += '      ' + prob[0]
    # print(line1)

    line2 = ''
    for prob in splitProbs:
        if line2 == '':
            line2 += prob[1] + ' ' + prob[2]
        else:
            line2 += '    ' + prob[1] + ' ' + prob[2]
    # print(line2)

    line3 = ''
    for prob in splitProbs:
        if line3 != '':
            line3 += '    '
        for x in range(0, len(prob[0]) + 2):
            line3 += '-'
    # print(line3)

    # find solutions
    sols = list()
    for prob in splitProbs:
        if prob[1] == '+':
            sols.append(int(prob[0]) + int(prob[2]))
        elif prob[1] == '-':
            sols.append(int(prob[0]) - int(prob[2]))
    # print(sols)

    # add blank space to solutions
    for i in range(0, len(sols)):
        while len(str(sols[i])) < (len(splitProbs[i][0]) + 2):
            sols[i] = ' ' + str(sols[i])
            # print('SOLUTIONS', sols)

    # create solution line
    line4 = ''
    for sol in sols:
        if line4 != '':
            line4 += '    ' + sol
        else:
            line4 += sol
    # print(line4)

    ## Put it all together!
    arranged_problems = line1 + '\n' + line2 + '\n' + line3
    if solution is True:
        arranged_problems += '\n' + line4

    return arranged_problems