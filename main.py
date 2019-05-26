import json

with open('config.json', 'r') as f:
    config_data = f.read()
config = json.loads(config_data)

with open('data.json', 'r') as e:
    acronym_data = e.read()
acronyms = json.loads(acronym_data)

def verify_web_hook(form):
    if not form or form.get('token') != config['SLACK_TOKEN']:
        raise ValueError('Invalid request/credentials.')

def search_acronyms(term):
    answer = []
    for a in acronyms:
        if str(term.upper()) in a:
            answer.append(a)
    if len(answer) > 1:
        values = ') or ('.join(str(a[f"{term}"]) for a in answer)
        message = f"{len(answer)} entries found: ({values})"
        return message
    elif len(answer) == 1:
        value = answer[0][f"{term}"]
        message = f"{len(answer)} entry found: ({value})"
        return message
    else:
        message = "No entries found for that acronym."
        return message

def acronym_bot(request):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    verify_web_hook(request.form)
    search_response = search_acronyms(request.form['text'])
    return search_response