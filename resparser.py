import requests
import json

superparser_api_key = ''
resume_file_path = 'AayaanHasnainResume.pdf'

def parse_resume_with_superparser(api_key, resume_path):
    url = 'https://api.superparser.com/parse'

    headers = {
        'X-API-Key': ""
    }

    files = {
        'file_name': open("AayaanHasnainResume.pdf", 'rb')
    }

    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def skills():

    parsed_resume = parse_resume_with_superparser(superparser_api_key, resume_file_path)
    # formatted_resume = json.dumps(parsed_resume, indent=4)

    overall_skills = []

    overall_skills = parsed_resume["data"]["skills"]["overall_skills"]

    return(overall_skills)

