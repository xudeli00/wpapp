import random
def count_20():
    op = random.choice(['+','-'])
    if op == '+':
        a = random.randint(2,9)
        if a < 10:
            b = random.randint(10 - a, 19 - a)
        else:
            b = random.randint(1, 20 - a)

        return (a, op, b)
    else:
        a = random.randint(10,18)
        b = random.randint(a - 9, 9)

        if a == b:
            a += 2
        return (a,op,b)

def main(count=20):

    all = []
    while True:
        rslt = count_20()
        if rslt not in all:
            all.append(rslt)

        if len(all) == count:
            break

    # for _math in all:
    #     print "%s %s %s =" % _math

    return all

