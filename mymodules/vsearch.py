def search4vowels(phrase:str) -> set:
    """ Returns vowels found in specified string """
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))


def search4letters(phrase:str, letters:str='aeiou') -> set:
    """ Returns letters found in specified string """
    return set(letters).intersection(set(phrase))
