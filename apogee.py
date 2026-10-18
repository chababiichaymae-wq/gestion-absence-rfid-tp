

#user doit entre leur num d'apogée :
def check_apogee(num_apogee: str) -> bool :
    num_apogee = num_apogee.strip()
    if num_apogee.isdigit() and len(num_apogee) == 7 :
        return True
    else :
        return False