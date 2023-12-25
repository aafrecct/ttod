from yaml import safe_load

# The game options are loaded.
with open('settings.yaml', 'r') as options_file:
    SETTINGS = safe_load(options_file)['options']


def load_questions():
    '''Returns a dictionary with the grouped questions in the given folder.
    Looks for files "truths.yaml" and "dares.yaml" inside the folder.

    Keyword arguments:
    path -- The path to the file containing the questions.
    '''
    questions = {'truths': {}, 'dares': {}}
    for key in questions:
        with open(
                f"{SETTINGS['data_path']}/question_sets/{SETTINGS['question_set']}/{key}.yaml",
                'r') as questionsfile:
            questions[key] = safe_load(questionsfile)
    return questions


def load_dialogs():
    with open(
            f"{SETTINGS['data_path']}/question_sets/{SETTINGS['question_set']}/tui_dialogs.yaml",
            'r') as dialogs_file:
        dialogs = safe_load(dialogs_file)
    return dialogs
