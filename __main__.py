from random import randint

people = ['Jorge', 'David', 'Younes', 'Carlos', 'Borja']

with open('./list', 'r') as file:
    questions = file.readlines()

truth = [i[2:] for i in questions if i [:2] == 'T-']
dares = [i for i in questions if i not in truth]

def main():
    flow = ''
    prsn = ''
    i = 0
    while (flow != 'q'):
        i += 1 if  flow != 's' else 0
        prsn = people[i%5]
        t = input(prsn + ': Truth or Dare? ') == 't' 
        td = truth[randint(0, 189)] if t else dares[randint(0, 179)]
        print(prsn + ": " + td)
        same_person = flow != 'n'
        flow = input('Press enter for next: ')

if __name__ == '__main__':
    main()
