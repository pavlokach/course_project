class Data:
    __link = 'https://api.darksky.net/forecast/1f1c351099874a0b925a89f198c779dc/49.8397,24.0297?units=si&lang=uk&exclude=currently,minutely,hourly,alerts,flags'
    cycle = 0

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        import json
        import urllib.request
        f = urllib.request.urlopen(self.__link)
        data = json.loads(f.read().decode("utf-8"))
        with open(self.filename, 'w', encoding="utf-8") as outfile:
            json.dump(data, outfile)

    def extract_from_file(self):
        import json
        with open(self.filename, 'r') as f:
            self.alldata = json.load(f)

    def extract_day_data(self):
        self.cycle += 1
        if self.cycle == 31:
            self.cycle = 1
        return self.alldata['daily']['data'][0]
        """[self.cycle - 1]"""

    def get_parameters(self):
        data = self.extract_day_data()
        self.temp = (data['temperatureMax'] + data['temperatureMin']) / 2
        self.press = data['pressure']
        self.precip = data['precipIntensity']
        self.humidity = data['humidity']
        self.wind = data['windSpeed']

    def all_things(self):
        from datetime import date
        today = str(date.today())[5:]
        print(today)

        with open("SKN.txt", "r", encoding="UTF-8") as f:
            parameters = []
            for iter in range(3):
                line = f.readline()
                while today not in line:
                    line = f.readline()
                print(1)
                parameters.append(line[8:].strip())

        def check_clouds(clouds):
            if clouds <= 5:
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

        def check_woth_const(parameters):
            hum, press, temp = float(parameters[0]), float(parameters[1]), float(parameters[2])
            global today_temp
            today_temp = self.temp
            today_press = self.press
            today_hum = self.humidity
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

        hum, press, temp = float(parameters[0]), float(parameters[1]), float(parameters[2])
        today_temp = self.temp
        today_press = self.press
        today_hum = self.humidity
        temp_dif = (((today_temp - temp) ** 2) / 2) ** 0.5
        hum_dif = (((today_hum - hum) ** 2) / 2) ** 0.5
        press_dif = (((today_press - self.press) ** 2) / 2) ** 0.5
        par_check = {1: 0, 2: 0, 3: 0, 4: 0}
        par_humidity = check_humidity(self.humidity - 20)
        par_press = check_press(self.press)
        par_precip = check_precip(self.precip)
        pars = [check_temp_dif(temp_dif), check_woth_const(parameters),
                check_wind(self.wind), par_humidity, par_precip, par_press]
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
        groups = {"Тиск": ["Гіпотонія", "Серцево-судинні захворювання", "Гіпертонія"],
                  "Температура": ["Цукровий діабет", "Астма"],
                  "Вологість": ["Гіпертонія", "Серцево-судинні захворювання"]}
        if par_humidity == 1: groups.pop("Тиск")
        if par_humidity == 1: groups.pop("Вологість")
        if today_temp == 1: groups.pop("Температура")
        if groups:
            reasons, diseases = [], []
            for key in groups:
                reasons.append(key)
                diseases.append(groups[key])

        return [[par_humidity, par_press, par_precip], out, summ, [reasons, diseases]]


"""
d = Data('data.json')
d.get_data()
d.extract_from_file()
print(d.extract_day_data())
d.get_parameters()
print(d.all_things())
"""
