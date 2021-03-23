from itertools import islice


def filter_intervals(intervals: list) -> list:
    """
    Filters given intervals by removing the ones that are already inside
    other intervals, and checking if there are overlapping intervals.

    :param intervals: unfiltered list of intervals
    :return: optimized list of intervals
    """
    # делим список на два отдельных списка одинаковой длины с,
    # соответственно, левыми и правыми границами интервалов
    left_borders = list(islice(intervals, 0, None, 2))
    right_borders = list(islice(intervals, 1, None, 2))
    # создаем список для отфильтрованных интервалов и записываем
    # туда начальные значения границ, с которыми будет производится
    # сравнение в первой итерации
    filtered_intervals = [left_borders[0], right_borders[0]]
    # проходим одним циклом по двум спискам
    for _ in range(len(intervals) // 2):
        if left_borders[_] < filtered_intervals[-1] < right_borders[_]:
            # проверяем, если последняя правая граница (а в списке
            # отфильтрованных границ последнее значение ВСЕГДА будет
            # правой границей) находится в пределах последующего интервала,
            # и если это так, "удлиняем" интервал, заменяя значение
            # правой границы
            filtered_intervals.pop()
            filtered_intervals.append(right_borders[_])
        elif left_borders[_] < right_borders[_] < filtered_intervals[-1]:
            # если обе границы последующего интервала меньше крайней
            # правой границы, значит, последующий интервал весь находится в
            # пределах уже записанного интервала, соответственно, ничего
            # не делаем, это дубль
            pass
        elif left_borders[_] > filtered_intervals[-1]:
            # если же левая граница последующего интервала больше текущей
            # крайней правой границы, значит, это уже новый интервал,
            # добавляем его к списку с отфильтрованными интервалами для
            # последующего сравнения
            filtered_intervals.extend([left_borders[_], right_borders[_]])
    return filtered_intervals


def appearance(intervals: dict) -> int:
    """
    Counts the appearance of pupils and tutors. Checks whether the intervals
    provided in seconds via a dictionary with lists correspond with each
    other. If they do, checks how exactly they do it and counts the
    appearance based on that.

    :param intervals: dictionary with lists of intervals
    :return: appearance on a lesson in seconds
    """
    lesson, pupils, tutors = intervals.values()
    pupils = filter_intervals(pupils)
    tutors = filter_intervals(tutors)
    counter_pupil = 0
    mutual_attendance = []
    total_attendance = 0
    while counter_pupil < len(pupils):
        counter_tutor = 0
        while counter_tutor < len(tutors):
            if lesson[0] in range(pupils[counter_pupil],
                                  pupils[counter_pupil + 1] + 1) and \
                    lesson[0] in range(tutors[counter_tutor],
                                       tutors[counter_tutor + 1] + 1):
                # проверка, если преподаватель и студент зашли на урок
                # раньше его начала
                mutual_attendance.append(lesson[0])
                mutual_attendance.append(tutors[counter_tutor + 1] if
                                         tutors[counter_tutor + 1] <
                                         pupils[counter_pupil + 1] else
                                         pupils[counter_pupil + 1])
            elif lesson[1] in range(pupils[counter_pupil],
                                    pupils[counter_pupil + 1] + 1) and \
                    lesson[1] in range(tutors[counter_tutor],
                                       tutors[counter_tutor + 1] + 1):
                # проверка, если преподаватель и студент остались на
                # уроке после его конца
                mutual_attendance.append(tutors[counter_tutor] if
                                         tutors[counter_tutor] >
                                         pupils[counter_pupil] else
                                         pupils[counter_pupil])
                mutual_attendance.append(lesson[1])
            elif tutors[counter_tutor + 1] < pupils[counter_pupil] or \
                    tutors[counter_tutor] > pupils[counter_pupil + 1]:
                # проверка, если два интервала вообще никак не пересекаются
                mutual_attendance.extend([0, 0])
            elif tutors[counter_tutor] in \
                    range(pupils[counter_pupil],
                          pupils[counter_pupil + 1] + 1) and tutors[
                counter_tutor + 1] in range(pupils[counter_pupil],
                                            pupils[counter_pupil + 1] + 1):
                # проверка, если один интервал полностью находится
                # внутри другого
                mutual_attendance.append(tutors[counter_tutor])
                mutual_attendance.append(tutors[counter_tutor + 1])
            elif pupils[counter_pupil] in \
                    range(tutors[counter_tutor],
                          tutors[counter_tutor + 1] + 1) and pupils[
                counter_pupil + 1] in range(tutors[counter_tutor],
                                            tutors[counter_tutor + 1] + 1):
                # аналогичная проверка для обратной ситуации
                mutual_attendance.append(pupils[counter_pupil])
                mutual_attendance.append(pupils[counter_pupil + 1])
            elif tutors[counter_tutor] <= pupils[counter_pupil] < tutors[
                counter_tutor + 1] < \
                    pupils[counter_pupil + 1]:
                # проверка, если правая граница одного из интервалов
                # находится внутри другого
                mutual_attendance.append(pupils[counter_pupil])
                mutual_attendance.append(tutors[counter_tutor + 1])
            elif pupils[counter_pupil] <= tutors[counter_tutor] < \
                    pupils[counter_pupil + 1] < tutors[counter_tutor + 1]:
                # аналогичная проверка для обратной ситуации
                mutual_attendance.append(tutors[counter_tutor])
                mutual_attendance.append(pupils[counter_pupil + 1])
            total_attendance += abs(
                mutual_attendance[1] - mutual_attendance[0])
            mutual_attendance.clear()
            counter_tutor += 2
        counter_pupil += 2
    return total_attendance


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389,
                        1594663390, 1594663395,
                        1594663396, 1594666472],
              'tutor': [1594663290, 1594663430,
                        1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500,
                        1594702807, 1594704542,
                        1594704512, 1594704513,
                        1594704564, 1594705150,
                        1594704581, 1594704582,
                        1594704734, 1594705009,
                        1594705095, 1594705096,
                        1594705106, 1594706480,
                        1594705158, 1594705773,
                        1594705849, 1594706480,
                        1594706500, 1594706875,
                        1594706502, 1594706503,
                        1594706524, 1594706524,
                        1594706579, 1594706641],
              'tutor': [1594700035, 1594700364,
                        1594702749, 1594705148,
                        1594705149, 1594706463]},
     'answer': 3577
     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066,
                        1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test[
            'answer'], f'Error on test case {i}, got {test_answer}, ' \
                       f'expected {test["answer"]}'
        print(test_answer)
