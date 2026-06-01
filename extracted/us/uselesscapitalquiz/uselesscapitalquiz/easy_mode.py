import random
from .lists import easy_country_list, easy_capital_list
def easy_mode():
    score = 0
    question_number = 0
    for i in range(1, 11):
        double_count_prevention = 0
        question = random.randint(0, (65 - question_number))
        country = ( easy_country_list[question] )
        capital = ( easy_capital_list[question] )
        capital_ask = input("\nEnter the capital of " + country + ": ")
        capital_ask = capital_ask.lower()
        country = country.lower()
        capital = capital.lower()
        if country == "south africa":
            if capital_ask == "cape town":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
            elif capital_ask == "pretoria":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_country_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
            elif capital_ask == "bloemfontein":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_country_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + easy_capital_list[question])
                easy_country_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
        if country == "bolivia":
            if capital_ask == "sucre":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
            elif capital_ask == "la paz":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + easy_capital_list[question])
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
                double_count_prevention = 1
        if double_count_prevention == 0:
            if capital_ask == capital:
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + easy_capital_list[question])
                easy_capital_list.pop(question)
                easy_country_list.pop(question)
    print("You got " + str(score) + " out of 10 questions correct on easy mode.")