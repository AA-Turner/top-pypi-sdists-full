import random
from .lists import hard_country_list, hard_capital_list
def hard_mode():
    score = 0
    question_number = 0
    for i in range(1, 11):
        double_count_prevention = 0
        question = random.randint(0, (63 - question_number))
        country = ( hard_country_list[question] )
        capital = ( hard_capital_list[question] )
        capital_ask = input("\nEnter the capital of " + country + ": ")
        capital_ask = capital_ask.lower()
        country = country.lower()
        capital = capital.lower()
        if country == "swaziland":
            if capital_ask == "lobamba":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "mbabane":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + hard_capital_list[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if country == "palau":
            if capital_ask == "ngerulmud":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            elif capital_ask == "melekeok":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + hard_capital_list[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if double_count_prevention == 0:
            if capital_ask == capital:
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                hard_capital_list.pop(question)
                hard_country_list.pop(question)
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + hard_capital_list[question])
                hard_capital_list.pop(question)
                hard_country_list.pop(question)
    print("You got " + str(score) + " out of 10 questions correct on Hard mode.")
