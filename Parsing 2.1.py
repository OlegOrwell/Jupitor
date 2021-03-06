from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json


main_link = 'https://hh.ru'
name = input("Enter profession name: ")
l = 1
p = 0

response = requests.get(main_link+"/vacancies/"+name, headers={'User-Agent': "Mozilla"})
jobs = []

while True:
    try:

        soup_big = bs(response.text,'lxml')
       # print(response)

        #soup = soup_big.find("div", class_=["vacancy-serp", "vacancy-serp-item vacancy-serp-item_premium"]).findChildren()

        elements = soup_big.find_all("div", class_="vacancy-serp-item")
        elements += soup_big.find_all("div", class_="vacancy-serp-item vacancy-serp-item_premium")

        for element in elements:
            job_data = {}
            job_data['name'] = element.find("a", class_="bloko-link HH-LinkModifier").getText()
            job_data['link'] = element.find("a", class_="bloko-link HH-LinkModifier")["href"]
            vacancy_salary = element.find("div", class_="vacancy-serp-item__sidebar").getText()

            min_salary = []
            max_salary = []
            currency = []
            happen = 0
            for i in vacancy_salary:
                if vacancy_salary[0].isnumeric() == False:
                    min_salary = "Договорная"
                    break
                else:
                    if i == "-":
                        happen = 1
                    if i.isnumeric() == True and happen == 0:
                        min_salary.append(i)
                    elif i.isnumeric() == True and happen == 1:
                        max_salary.append(i)
                    elif i.isalpha() == True:
                        currency.append(i)
            min_salary = ''.join(min_salary)
            max_salary = ''.join(max_salary)
            currency = ''.join(currency)
            job_data['salary_min'] = min_salary
            job_data['salary_max'] = max_salary
            job_data['currency'] = currency
            job_data["common_url"] = main_link

            jobs.append(job_data)
            p = p + 1


        contin = soup_big.find("a", class_="bloko-button HH-Pager-Controls-Next HH-Pager-Control")
        url_continue = soup_big.find("a", class_="bloko-button HH-Pager-Controls-Next HH-Pager-Control")["href"]
        url_cont = main_link+url_continue

        print(url_cont)
        params = {'page': 'l'}
        response = requests.get(url_cont, headers={'User-Agent': "Mozilla"})

        l = l + 1

    except:
        break

print(p, " анкеты собрано ")
print(jobs)

out_file = open("proffies.json", "w")
json.dump(jobs, out_file, indent=6)
out_file.close()