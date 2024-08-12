from safe_call import safe


@safe(False)
def GetInputOrExit(question, validator):
    while True:
        input_value = input(question)
        if (input_value == "exit"):
            return None
        if (not validator(input_value)):
            print("Verify your input and try again!")
            continue
        return input_value
    