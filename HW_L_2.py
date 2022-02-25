import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

main_link = 'https://superjob.ru'

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
              'Authorization': '*/*'}

vacancy_input = input('Введите название вакансии: ')
vacancies = []
pages_input = int(input('Введите количество анализируемых страниц. Для анализа по всем страницам поиска введите 0: '))

params = {'keywords': vacancy_input,
          'page': ''}

response = requests.get(main_link + '/vacancy/search/', headers=header, params=params)

if response.ok:
    soup = bs(response.text, 'html.parser')
    if pages_input == 0:
        page_block = soup.find('a', {'class': 'f-test-button-1'})
        if not page_block:
            last_page = 1
        else:
            page_block = page_block.findParent()
            last_page = int(page_block.find_all('a')[-2].getText())
    else:
        last_page = pages_input

    for page in range(last_page):
        params['page'] = page
        html = requests.get(main_link + '/vacancy/search/', headers=header, params=params)

        if html.ok:
            parsed_html = bs(html.text, 'html.parser')

            vacancy_list = parsed_html.findAll('div', {'class': 'Fo44F QiY08 LvoDO'}) #Check before use

            for vacancy in vacancy_list:
                vacancy_data = {}
                vacancy_link = main_link + vacancy.find('div', {'class': 'jNMYr GPKTZ _1tH7S'}).find('a')['href']   #Check before use
                vacancy_name = vacancy.find('span', {'class': '_3a-0Y _3DjcL _3sM6i'}).getText() #Check before use
                vacancy_salary = vacancy.find('span', {'class': '_1OuF_ _1qw9T f-test-text-company-item-salary'}).getText() #Check before use
                if vacancy.find('span', {'class': '_3Fsn4 f-test-text-vacancy-item-company-name _1_OKi _3DjcL _1tCB5 _3fXVo _2iyjv'}):
                    vacancy_company = vacancy.find('span', {'class': '_3Fsn4 f-test-text-vacancy-item-company-name _1_OKi _3DjcL _1tCB5 _3fXVo _2iyjv'}).find('a').getText()
                else:
                    vacancy_company = 'NaN'
                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = vacancy_link
                vacancy_data['company'] = vacancy_company
                vacancy_salary_list = vacancy_salary.split( )

                if vacancy_salary_list[0] == 'от':
                    vacancy_data['salary_min'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
                    vacancy_data['salary_max'] = 'NaN'
                    vacancy_data['currency'] = vacancy_salary_list[3]
                elif vacancy_salary_list[0] == 'до':
                    vacancy_data['salary_min'] = 'NaN'
                    vacancy_data['salary_max'] = int(vacancy_salary_list[1] + vacancy_salary_list[2])
                    vacancy_data['currency'] = vacancy_salary_list[3]
                elif vacancy_salary_list[0] == 'По':
                    vacancy_data['salary_min'] = 'NaN'
                    vacancy_data['salary_max'] = 'NaN'
                    vacancy_data['currency'] = 'NaN'
                elif vacancy_salary.find('-') & len(vacancy_salary_list) > 4:
                    vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
                    vacancy_data['salary_max'] = int(vacancy_salary_list[3] + vacancy_salary_list[4])
                    vacancy_data['currency'] = vacancy_salary_list[4]
                else:
                    vacancy_data['salary_min'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
                    vacancy_data['salary_max'] = int(vacancy_salary_list[0] + vacancy_salary_list[1])
                    vacancy_data['currency'] = vacancy_salary_list[2]

                vacancy_data['source'] = main_link[15:]
                vacancies.append(vacancy_data)

                if not soup.find('a', {'class': 'icMQ_ bs_sM _3ze9n l9LnJ f-test-button-dalshe f-test-link-Dalshe'}):
                    break


df_vacancies = pd.DataFrame(vacancies)
df_vacancies.to_csv(f'df_vacancies_sj_{vacancy_input}.csv', encoding='utf-8')