from wikipediaapi import Wikipedia, Namespace


def get_russian_category_members(category_members: dict) -> list:
    """
    Returns the Russian names of categories. Receives a dictionary
    with all the category members and iterates over it, checking
    if the name of the category member fits the parameters.

    :param category_members: dictionary received from the Wikipedia API
    :return: list with Russian names
    """
    names = []
    for c in category_members.values():
        # логика выборки тут следующая - отсекаются подкатегории, потом
        # отсекаются все англоязычные категории, после этого отсекаются
        # все названия, заканчивающиеся на ) - например, (семейство),
        # (род) и т.п., также отсекаются названия, заканчивающиеся на
        # "ы" и "и" - на вики туда попадают, в основном, различные
        # семейства и рода животных, есть редкие исключения, например,
        # "окапи", но их так мало, что я решил ими пренебречь
        if c.ns == Namespace.MAIN and ord(c.title[:1].upper()) >= 1040 \
                and c.title[-1:] not in (')', 'ы', 'и') \
                and c.title[-2:] != 'ые':
            names.append(c.title)
    return names


def count_names(names_list: list) -> dict:
    """
    Counts the names of the category members from the given list.

    :param names_list: list of category members
    :return: dictionary where key is a letter of Russian alphabet and value is
    the number of the category members starting with that letter.
    """
    alphabet_dict = {
        "А": 0,
        "Б": 0,
        "В": 0,
        "Г": 0,
        "Д": 0,
        "Е": 0,
        "Ё": 0,
        "Ж": 0,
        "З": 0,
        "И": 0,
        "Й": 0,
        "К": 0,
        "Л": 0,
        "М": 0,
        "Н": 0,
        "О": 0,
        "П": 0,
        "Р": 0,
        "С": 0,
        "Т": 0,
        "У": 0,
        "Ф": 0,
        "Х": 0,
        "Ц": 0,
        "Ч": 0,
        "Ш": 0,
        "Щ": 0,
        "Э": 0,
        "Ю": 0,
        "Я": 0
    }
    for name in names_list:
        alphabet_dict[name[:1].upper()] += 1
    return alphabet_dict


wiki_wiki = Wikipedia('ru')
members = wiki_wiki.page('Категория:Животные по алфавиту').categorymembers
animal_names = get_russian_category_members(members)
counted_names = count_names(animal_names)
for key, value in counted_names.items():
    print(f'{key}: {value}')
