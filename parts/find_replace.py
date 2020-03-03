find_replace = [
    " c.; cup",
    " qt.; quart",
    "12 cup;1/2 cup",
    "13 cup;1/3 cup",
    "14 cup;1/4 cup",
    "18 cup;1/8 cup",
    "23 cup;2/3 cup",
    "34 cup;3/4 cup",
    "12 tables;1/2 tables",
    "12 teasp;1/2 teasp",
    "13 teasp;1/3 teasp",
    "14 teasp;1/4 teasp",
    "18 teasp;1/8 teasp",
    "34 teasp;3/4 teasp",
    "12 liter;1/2 liter",
    " Qt.; quart",
    "12 Cup;1/2 cup",
    "13 Cup;1/3 cup",
    "14 Cup;1/4 cup",
    "18 Cup;1/8 cup",
    "23 Cup;2/3 cup",
    "34 Cup;3/4 cup",
    "12 Tables;1/2 tables",
    "12 Teasp;1/2 teasp",
    "13 Teasp;1/3 teasp",
    "14 Teasp;1/4 teasp",
    "18 Teasp;1/8 teasp",
    "34 Teasp;3/4 teasp",
    "12 Liter;1/2 liter"
]

f = open('data/layer1original.json', 'r')
# f = open('test.txt', 'r')
all_recipies = f.read().splitlines()
f.close()

f = open('data/layer1.json', 'w')
# f = open('test2.txt', 'w')
for line in all_recipies:
    for fr in find_replace:
        fr = fr.split(";")
        if fr[0] in line:
            line =line.replace(fr[0], fr[1])
    f.write(line)
    f.write('\n')
f.close()