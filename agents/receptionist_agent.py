def generate_followup_questions(patient):
    name = patient['patient_name']
    diagnosis = patient['primary_diagnosis']
    meds = ", ".join(patient['medications'])
    diet = patient['dietary_restrictions']

    questions = (
        f"Hi {name}! I'm your post-discharge assistant.\n\n"
        f"I see you were discharged for **{diagnosis}**.\n"
        f"Are you taking your medications ({meds}) as prescribed?\n"
        f"Are you following your dietary guidelines: {diet}?\n"
        f"Please describe any symptoms or questions you have below:"
    )
    return questions
