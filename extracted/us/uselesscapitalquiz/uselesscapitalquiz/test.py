import random
def quiz_makes(list, anwsers, length):
    score = 0
    question_number = 0
    leng = len(list)
    lengy = len(anwsers)
    if leng != lengy:
        print('Error: there must be the same amount of things in each list ')
        quit()
    if length  > lengy:
        print('Error: the length of the quiz must be equal to or shorter than the lists ')
        quit()

    for i in range(0, length):
        question = random.randint(0, (lengy-1 - question_number))
        prompt = ( list[question] )
        correct = ( anwsers[question] )
        question_ask = input("\nEnter the anwser to " + prompt +": ")
        question_ask = question_ask.lower()
        correct = correct.lower()
        if question_ask == correct:
            score += 1
            question_number += 1
            print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
            print(question)
            list.pop(question)
            anwsers.pop(question)
        else:
            question_number += 1
            print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + anwsers[question])
            list.pop(question)
            anwsers.pop(question)
    print("You got " + str(score) + " out of " +str(lengy) + " questions correct.")

