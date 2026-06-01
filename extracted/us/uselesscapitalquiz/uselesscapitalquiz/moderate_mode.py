import random
from .lists import moderate_capital_list, moderate_country_list

def moderate_mode():
    score = 0
    question_number = 0
    for i in range(1, 11):
        double_count_prevention = 0
        question = random.randint(0, (65 - question_number))
        country = ( moderate_country_list[question] )
        capital = ( moderate_capital_list[question] )
        capital_ask = input("\nEnter the capital of " + country + ": ")
        capital_ask = capital_ask.lower()
        country = country.lower()
        capital = capital.lower()
        if country == "sri lanka":
            if capital_ask == "sri jayawardenepura kotte":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                moderate_country_list.pop(question)
                moderate_capital_list.pop(question)
                double_count_prevention = 1
            elif capital_ask == "kotte":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                moderate_capital_list.pop(question)
                moderate_country_list.pop(question)
                double_count_prevention = 1
            elif capital_ask == "colombo":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                moderate_capital_list.pop(question)
                moderate_country_list.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + moderate_country_list[question])
                moderate_capital_list.pop(question)
                moderate_country_list.pop(question)
                double_count_prevention = 1
        if double_count_prevention == 0:
            if capital_ask == capital:
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                moderate_capital_list.pop(question)
                moderate_country_list.pop(question)
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + moderate_capital_list[question])
                moderate_capital_list.pop(question)
                moderate_country_list.pop(question)
    print("You got " + str(score) + " out of 10 questions correct on Moderate mode.")