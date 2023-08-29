import cohere
from resparser import skills

api_key = ""

co = cohere.Client(api_key=api_key)

def ask_question(prompt):

    response = co.generate(
        model="base-light",
        prompt=prompt,
        max_tokens = 70
    )

    return response[0].text


def interview(tech_skills):
    name = "Aayaan"
    responses = {}

    for skill in tech_skills:
        tech_question = ask_question(f"Imagine you are the interviewer of {name}, and you are interviewing them on this {skill}. Generate a question on the {skill} provided making sure its not hard and can be answered in one word")
        print(tech_question)
        user_response = input()
        responses[tech_question] = user_response
    

    motivation_question = ask_question("Imagine you are the interviewer of {name}, and you want to test out their inner motivation to work for the company, ask a question for the interviewer on this aspect ")
    user_response = input(motivation_question)
    responses[motivation_question] = user_response


    behavioral_question = ask_question("Imagine you are the interviewer of {name}, and you want to test out their behaviour towards projects , generate a question for the interviewer on this aspect ")
    user_response = input(motivation_question)
    responses[behavioral_question] = user_response

    return responses

tech_skills = []
tech_skills = skills()
tech_skills = tech_skills[:1]

responses = interview(tech_skills)

for question, response in responses.items():
    print(f"Question: {question}")
    print(f"Response: {response}")