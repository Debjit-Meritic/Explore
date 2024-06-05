from openai import OpenAI
import os
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

def get_summary(system_prompt, user_prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5, 
    )
    return response.choices[0].message.content

def review_summary(system_prompt, user_prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5, 
    )
    return response.choices[0].message.content

system_prompt1 = f"""
PERSONA :
You are a financial analyst, responsible for writing financial commentaries from the data and guidelines provided, for the chief financial officer of the company. You strictly follow the output format. You are diligent, precise and succinct.

GUIDELINES :
- You are doing variance analysis commentary for actuals vs forecasts. If the variance is <5% (actuals underperform or overperform vs forecasts), \
    the commentary should quantify this to be a minor miss or minor achievement. If the variance is >15%,the commentary should quantify this as a \
    major miss or major achievement.
- When focusing on deep dive attributes that were major contributors in variance, mention both the attributes that lead to overperformance and attributes \
    that led to underperformance. Talk first about attributes for underperformance if actuals were less than target and talk first about attributes for \
    overperformance if actuals were more than target.
- Prioritise absolute values over percentages. E.g. mention that target missed actuals by $xM first and then talk about the % miss.

OUTPUT FORMAT :
Return the summary as a json with key summary.
Keep the summary in a single paragraph with at most 7 lines.
Note that a line is defined as a sentence ending with a period symbol(.).
"""

metric_analysis = f"""
METRIC INFORMATION :
Total Cash Receipts for [PILLAR='OE Adult', MONTH_YEAR>='2023-10-01']
Metric value is $6.51M

ANALYSIS INFORMATION :
ANALYSIS NEXT STEP - Compare the metric against Forecast
ANALYSIS RESULTS - 
    - Metric value was $6.51M vs Forecast was $7.36M. Metric underperformed by $857.49K, 12% of the Forecast.
    - ANALYSIS NEXT STEP - Decide to split the metric by the dimension LOCATION.
ANALYSIS RESULTS - 
    - There are 11 unique values of the dimension LOCATION
    - Colombia, Brazil, US Hispanic contribute to 41% of the metric variance.
    - Colombia actual was $637.87K and Forecast was $908.53K. Variance was ($270,661.00), missing target by 30%, which contributes 32% to the total variance.
    - Brazil actual was $1.18M and Forecast was $1.33M. Variance was ($145,031.00), missing target by 11%, which contributes 17% to the total variance.
    - US Hispanic actual was $1.64M and Forecast was $1.58M. Variance was $60.68K, exceeding target by 4%, which contributes -7% to the total variance.
    - ANALYSIS NEXT STEP - Choose 'Colombia' to dive deeper because they make 32% of the variance. Split by the dimension CASHRECEIPTTYPE.
    - ANALYSIS RESULTS - 
        - For 'Colombia', There are 7 unique values of the dimension CASHRECEIPTTYPE
        - For 'Colombia', New Cash, Installments contribute to 79% of the metric variance.
        - For 'Colombia', New Cash actual was $293.31K and Forecast was $558.27K. Variance was ($264,968.00), missing target by 47%, which contributes 89% to the total variance.
        - For 'Colombia', Installments actual was $65.27K and Forecast was $34.58K. Variance was $30.69K, exceeding target by 89%, which contributes -10% to the total variance.
    - ANALYSIS NEXT STEP - Choose 'Brazil' to dive deeper because they make 17% of the variance. Split by the dimension CASHRECEIPTTYPE.
    - ANALYSIS RESULTS - 
        - For 'Brazil', There are 4 unique values of the dimension CASHRECEIPTTYPE
        - For 'Brazil', New Cash contribute to 93% of the metric variance.
        - For 'Brazil', New Cash actual was $868.85K and Forecast was $1.05M. Variance was ($176,906.00), missing target by 17%, which contributes 93% to the total variance.
    - ANALYSIS NEXT STEP - Choose 'US Hispanic' to dive deeper because they make -7% of the variance. Split by the dimension CASHRECEIPTTYPE.
    - ANALYSIS RESULTS - 
        - For 'US Hispanic', There are 7 unique values of the dimension CASHRECEIPTTYPE
        - For 'US Hispanic', Installments, New Cash contribute to 162% of the metric variance.
        - For 'US Hispanic', Installments actual was $518.53K and Forecast was $341.33K. Variance was $177.20K, exceeding target by 52%, which contributes 312% to the total variance.
        - For 'US Hispanic', New Cash actual was $495.24K and Forecast was $580.49K. Variance was ($85,244.00), missing target by 15%, which contributes -150% to the total variance.
    - ANALYSIS NEXT STEP - Decide to split the metric by the dimension CASHRECEIPTTYPE.
    - ANALYSIS RESULTS - 
        - There are 7 unique values of the dimension CASHRECEIPTTYPE
        - New Cash, Installments contribute to 82% of the metric variance.
        - New Cash actual was $2.95M and Forecast was $3.90M. Variance was ($946,386.00), missing target by 24%, which contributes 100% to the total variance.
        - Installments actual was $796.03K and Forecast was $622.64K. Variance was $173.40K, exceeding target by 28%, which contributes -18% to the total variance.
    - ANALYSIS NEXT STEP - Choose 'New Cash' to dive deeper because they make 100% of the variance. Split by the dimension LOCATION.
    - ANALYSIS RESULTS - 
        - For 'New Cash', There are 11 unique values of the dimension LOCATION
        - For 'New Cash', Colombia contribute to 28% of the metric variance.
        - For 'New Cash', Colombia actual was $293.31K and Forecast was $558.27K. Variance was ($264,968.00), missing target by 47%, which contributes 28% to the total variance.
    - ANALYSIS NEXT STEP - Choose 'Installments' to dive deeper because they make -18% of the variance. Split by the dimension LOCATION.
    - ANALYSIS RESULTS - 
        - For 'Installments', There are 11 unique values of the dimension LOCATION
        - For 'Installments', US Hispanic, LatAm Other contribute to 93% of the metric variance.
        - For 'Installments', US Hispanic actual was $518.53K and Forecast was $341.33K. Variance was $177.20K, exceeding target by 52%, which contributes 102% to the total variance.
        - For 'Installments', LatAm Other actual was $47.87K and Forecast was $64.32K. Variance was ($16,447.00), missing target by 26%, which contributes -10% to the total variance.
"""

response = ""

system_prompt2 = f"""
ROLE:
Your job is to validate the given summary which was generated on the given data. Follow the instructions provided and return output to the user STRICTLY in the format given.  

CONTEXT:
The data provided is the variance analysis of a financial metric. 
The summary provided was generated based on the given data. The purpose of the summary is to help financial analysts realise the cause of variance.  

INSTRUCTION:
1. Identify the main points mentioned in data and create a list of them.
2. Check if all these points are mentioned in the summary. Based on this, give a fractional \
    "Completeness" score to the entire summary. The score should be the number of points mentioned in the summary out of the number of points in the list. 
3. Create a list of numerical instances and validate every instance of a numerical value in the summary by checking with the data. \
    Based on this, give a fractional "Numerical Integrity" score to the entire summary. The score should be the number of numerical values \
    the summary got right out of the total number of numerical figures mentioned in the summary.
4. Give a "Crispness" score to the entire summary based on how succinct and crisp it is. 
5. Return the final output in the mentioned format to the user.

OUTPUT FORMAT:
Return a json with the following keys and values-
    "Main Points": the list of main points generated in step 1.
    "Completeness": the value of the "Completeness score generated in step 2 STRICTLY as a fraction.
    "Numerical Instances": the list of numerical instances created in step 3.
    "Numerical Integrity": the value of the "Numerical Integrity" score generated in step 3 STRICTLY as a fraction.
    "Crispness": the value of the cripsness score generated in step 4 STRICTLY as a percentage.

The fractional scores should be in the form of a fraction a/b where a and b are both integers.
"""
user_prompt2 = """
Provided below is the data of the variance analysis performed on the metric enclosed in triple backticks followed by the summary generated on this data.
Data: ```{data}```
Summary: ```{summary}```
"""



line_count = []
completeness_N = []
completeness_D = []
numerical_integrity_N = []
numerical_integrity_D = []
crispness = []

for i in range(1, 11):
    response_json = get_summary(system_prompt=system_prompt1, user_prompt=metric_analysis)
    response = json.loads(response_json)["summary"]
    print(str(i) + ":\n" + response + "\n")
    print("line_count: " + str(len(response.split(". "))))
    line_count.append(len(response.split(". ")))

    review_json = review_summary(system_prompt=system_prompt2, user_prompt=user_prompt2.format(data = metric_analysis, summary = response))
    print(review_json)
    review = json.loads(review_json)
    completeness_score = review["Completeness"].split("/")
    completeness_N.append(int(completeness_score[0]))
    completeness_D.append(int(completeness_score[1]))
    Numerical_Integrity_score = review["Numerical Integrity"].split("/")
    numerical_integrity_N.append(int(completeness_score[0]))
    numerical_integrity_D.append(int(completeness_score[1]))
    crispness.append(float(review["Crispness"].split("%")[0]))
    # for line in response.split(". "):
    #     print(line)
    # print("\n")
print("avg line count: " + str(sum(line_count)/len(line_count)))
print("avg completeness: ") + str(sum(completeness_N)/sum(completeness_D))
print("avg numerical integrity: " + str(sum(numerical_integrity_N)/sum(numerical_integrity_D)))
print("avg crispness: " + str(sum(crispness)/len(crispness)))

