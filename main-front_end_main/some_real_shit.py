from datetime import date, timedelta
import json

input_file = 'tester.json'
feb_flux = 76.9
feb_spots = 22


def swap(line):
    line1 = line.split('-')
    line1[0], line1[1] = line1[1], line1[0]
    return '-'.join(line1)


def jsonstuff(today, day):
    flux, spots = 0, 0
    with open(input_file, 'r', encoding='UTF-8') as data_file:
        data = json.load(data_file)[cycle]
    parameters, spaces = [], []

    with open('SKN.txt', 'r', encoding='UTF-8') as f:
        for iter in range(3):
            line = f.readline()
            while str(today) not in line:
                line = f.readline()
            parameters.append(line[8:].strip())
    if cycle <= 7:
        with open('space.txt', 'r', encoding='UTF-8') as f:
            while str(day) not in line:
                line = f.readline()
            spaces = line[6:].strip().split(';')
        spots, flux = int(spaces[0]), int(spaces[1])

    def check_clouds(clouds):
        if clouds < + 5:
            return 1
        elif clouds >= 8:
            return 3
        else:
            return 2

    def check_humidity(hum):
        if hum >= 45 and hum <= 70:
            return 1
        elif (hum >= 45 and hum <= 35) or (hum >= 75 and hum <= 85):
            return 2
        else:
            return 3

    def check_precip(precip):
        try:
            if precip == 502:
                return 3
            elif precip > 500:
                return 1
            else:
                return 2
        except:
            return 1

    def check_press(press):
        if press >= 988 or press <= 965:
            return 3
        elif press > 965 and press < 975:
            return 1
        else:
            return 2

    def check_wind(wind):
        if wind >= 10:
            return 3
        elif wind >= 3 and wind <= 5:
            return 1
        else:
            return 2

    def check_spots(spots=0):
        if cycle >= 7:
            return 4
        else:
            if spots < 0.75 * feb_spots:
                return 1
            elif spots > 1.25 * feb_spots:
                return 3
            else:
                return 2

    def check_flux(flux=0):
        if cycle >= 7:
            return 4
        else:
            if flux <= feb_flux:
                return 1
            elif flux > 1.25 * feb_flux:
                return 3
            else:
                return 2

    def check_woth_const(parameters):
        hum, press, temp = float(parameters[0]), float(parameters[1]), float(parameters[2])
        global today_temp
        today_temp = float(data['main']['temp'])
        today_press = float(data['main']['pressure'])
        today_hum = float(data['main']['humidity'])
        temp_dif = (((today_temp - temp) ** 2) / 2) ** 0.5
        hum_dif = (((today_hum - hum) ** 2) / 2) ** 0.5
        press_dif = (((today_press - press) ** 2) / 2) ** 0.5
        if min([temp_dif, hum_dif, press_dif]) > 5:
            return 3
        else:
            return 2

    def check_temp_dif(temp_dif):
        if temp_dif < 3:
            return 1
        elif temp_dif > 5:
            return 3
        else:
            return 2

    par_check = {1: 0, 2: 0, 3: 0, 4: 0}
    temp_dif = data['main']['temp_max'] - data['main']['temp_min']
    press = data['main']['pressure']
    clouds = data['clouds']['all'] / 10
    wind = data['wind']['speed']
    hum = data['main']['humidity']
    precip = data['weather'][0]['id']
    par_humidity = check_humidity(hum - 20)
    par_press = check_press(press)
    par_precip = check_precip(precip)
    pars = [check_spots(spots), check_flux(flux), check_temp_dif(temp_dif),
            check_woth_const(parameters), check_clouds(clouds),
            check_wind(wind), par_humidity, par_precip, par_press]
    for elem in pars:
        par_check[elem] += 1
    if par_check[3] != 0:
        if (par_check[2] != 0 or par_check[1] != 0) and par_check[2] >= 3:
            out = 2.5
        elif par_check[3] >= 3:
            out = 3
    else:
        if par_check[2] == 0:
            out = 1
        elif par_check[1] != 0 and par_check[1] >= 3:
            out = 1.5
        else:
            out = 2
    try:
        out += 1
        out -= 1
    except:
        out = 1.5
    summ = 0
    for key in par_check:
        summ += par_check[key] * key
    groups = {'Тиск': ['Гіпотонія', 'Серцево-судинні захворювання', 'Гіпертонія'],
              'Температура': ['Цукровий діабет', 'Астма'],
              'Вологість': ['Гіпертонія', 'Серцево-судинні захворювання']}
    if par_humidity == 1: groups.pop('Тиск')
    if par_humidity == 1: groups.pop('Вологість')
    if today_temp == 1: groups.pop('Температура')
    if groups:
        reasons, diseases = [], []
        for key in groups:
            reasons.append(key)
            diseases.append(groups[key])
    return [[par_humidity, par_press, par_precip], out, summ, [reasons, diseases]]

kpcc = 0
cycle = 0
bigdic = {}
today = date.today()
day = date.today()
day -= timedelta(int(str(day)[8:]) + 1)
for i in range(50):
    kpcc += 1
    cycle += 1
    print(today)
    try:
        for_time = jsonstuff(str(today)[5:], swap(str(day)[5:]))
    except:
        print('#####', today)
        break
    bigdic[str(today)] = [for_time[0]]
    bigdic[str(today)].append(for_time[1])
    bigdic[str(today)].append(for_time[2])
    bigdic[str(today)].append(for_time[3])
    today += timedelta(1)
    # print(today)
    # print(int(date(today.split[0])), int(date(today.split[1])), int(date(today.split[2])))
    day += timedelta(1)
    # print(day)
# print(bigdic)
with open('info.json', 'w', encoding='utf8') as f:
    f.write(str(bigdic).replace("'", '"'))
print(kpcc)