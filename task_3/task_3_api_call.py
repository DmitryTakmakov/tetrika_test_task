from requests import post

test_values = {'lesson': [1594663200, 1594666800],
               'pupil': [1594663340, 1594663389,
                         1594663390, 1594663395,
                         1594663396, 1594666472],
               'tutor': [1594663290, 1594663430,
                         1594663443, 1594666473]}

resp = post('http://127.0.0.1:7777/api/', json=test_values)
print(resp.json())
