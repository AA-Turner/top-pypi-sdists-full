import random
from .lists import  list_capitals, list_countries
def all():
    score = 0
    question_number = 0
    for i in range(1, 11):
        double_count_prevention = 0
        question = random.randint(0, (195 - question_number))
        country = ( list_countries[question] )
        capital = ( list_capitals[question] )
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
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if country == "bolivia":
            if capital_ask == "sucre":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "la paz":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if country == "Palau":
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
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if country == "sri lanka":
            if capital_ask == "sri jayawardenepura kotte":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "kotte":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "colombo":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if country == "south africa":
            if capital_ask == "cape town":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "pretoria":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_countries.pop(question)
                list_capitals.pop(question)
                double_count_prevention = 1
            elif capital_ask == "bloemfontein":
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
                double_count_prevention = 1
        if double_count_prevention == 0:
            if capital_ask == capital:
                score += 1
                question_number += 1
                print("You are correct! You have gotten " + str(score) + " out of " + str(question_number) + " questions correct!")
                list_capitals.pop(question)
                list_countries.pop(question)
            else:
                question_number += 1
                print("You are incorrect. You have gotten " + str(score) + " out of " + str(question_number) + " questions correct. The correct anwser was " + list_capitals[question])
                list_capitals.pop(question)
                list_countries.pop(question)
    print("You got " + str(score) + " out of 10 questions correct on all mode.")