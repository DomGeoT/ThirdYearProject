def pushValue(stack, value):
    if (not isinstance(int(v, int))) or value < 0 or value > (2 ** 20) -1:
        return -1
    stack.append(value)


def compute(instr, stack):
    print(instr, stack)
    if instr == 'POP':
        value = -1
        for i in range(len(stack) - 1, 0, -1): # remove 'topmost number' therefore skip over instructions till int is found
            if isinstance(stack[i], int):
                value = stack.pop(i)
                break # int found so stop searching
        if value == -1:
            return -1 # no int to pop therefore return error
    elif instr == 'DUP':

        dup = False
        for i in range(len(stack) - 1, 0, -1):  # remove 'topmost number' therefore skip over instructions till int is found
            if isinstance(stack[i], int):
                value = stack.append(stack[i])
                break  # int found so stop searching
        if not dup:
            return -1  # no int to dup therefore return error

        stack.append(stack[len(stack) - 1])
    elif instr == '+':
        op1 = stack.pop()
        op2 = stack.pop()
        stack.append(op1 + op2)
    elif instr == '-':
        op1 = stack.pop()
        op2 = stack.pop()
        stack.append(op1 - op2)
    else:
        if (not isinstance(int(instr, int)) or int(instr) < 0 or int(instr > (2 ** 20) -1):
            return -1
        stack.append(int(instr))
    print(stack)
    print()
    return stack


def solution(S):
    remainingInstr = S
    stack = []

    while True:
        splitInstr = remainingInstr.split(" ", 1)
        print(splitInstr)
        if len(splitInstr) == 1:
            return compute(splitInstr[0], stack).pop()

        stack = compute(splitInstr[0], stack)
        remainingInstr = splitInstr[1]

