import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    male_data = df[df['sex']=='Male']
    average_age_men = male_data['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    edu_counts = df['education'].value_counts()
    percentage_bachelors = ((edu_counts['Bachelors'] / len(df)) * 100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    higher_ed_salary = higher_education['salary'].value_counts()
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_ed_salary = lower_education['salary'].value_counts()

    # percentage with salary >50K
    higher_education_rich = ((higher_ed_salary['>50K'] / len(higher_education)) * 100).round(1)
    lower_education_rich = ((lower_ed_salary['>50K'] / len(lower_education)) * 100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    min_work_data = df[df['hours-per-week']==min_work_hours]

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(min_work_data)

    min_work_salary = min_work_data['salary'].value_counts()
    rich_percentage = ((min_work_salary['>50K']/num_min_workers) * 100).round(1)

    # What country has the highest percentage of people that earn >50K?
    country_vs_richperc = pd.DataFrame(columns = ['country', 'rich_percentage'])
    countries = df['native-country'].unique()
    for country in countries:
      country_tempdf = df[df['native-country']==country]
      salary_nums = country_tempdf['salary'].value_counts()
      try:
        rich_perc_country = ((salary_nums['>50K']/len(country_tempdf)) * 100).round(1)
      except:
        rich_perc_country = 0
      data_to_append = pd.DataFrame({'country':[country], 'rich_percentage':[rich_perc_country]})
      country_vs_richperc = pd.concat([country_vs_richperc, data_to_append], ignore_index = True)
  
    highest_earning_country = country_vs_richperc.loc[country_vs_richperc['rich_percentage'].idxmax()]['country']
    highest_earning_country_percentage = country_vs_richperc['rich_percentage'].max()

    # Identify the most popular occupation for those who earn >50K in India.

    India_data = df[df['native-country'] == 'India']
    India_occs = India_data['occupation'].value_counts()
    print(India_occs)
    top_IN_occupation = India_occs.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
